import datetime
from pathlib import Path
from typing import List, Set, Tuple, Union

import dagstermill as dm
import spacy
from dagster import GraphIn, GraphOut, In, Nothing, Out, Output, graph, job, op
from sklearn.model_selection import train_test_split
from spacy.cli.train import train as spacy_train
from spacy.scorer import Scorer
from spacy.tokens import DocBin
from spacy.training import Example

import jobs.common.bigquery as bq
from jobs.common.types import Records
from jobs.definitions import ROOT_DIR

nlp = spacy.load("en_core_web_md")

Dataset = List[Tuple[str, Tuple[str, str]]]


def prefix_dict(d: dict, prefix: str):
    return {f"{prefix}_{k}": v for k, v in d.items()}


def stringify_nested(d):
    return {k: str(v) if isinstance(v, dict) else v for k, v in d.items()}


def get_latest_model(model_name: str) -> Path:
    model_folder = ROOT_DIR / "models" / model_name
    for level in ["year", "month", "day"]:
        model_folder = model_folder / max(
            x.name for x in model_folder.iterdir() if x.is_dir()
        )
    return model_folder


def make_docs(data: Dataset, tgt_file: Union[str, Path], cats: Set[str]):
    docs = DocBin()
    for doc, (_, label) in nlp.pipe(data, as_tuples=True):
        for cat in cats:
            doc.cats[cat] = 1 if cat == label else 0
        docs.add(doc)
    docs.to_disk(tgt_file)
    return docs


def score_text_cat(model_path: Path, data: Dataset, cats: Set[str]):
    nlp_textcat = spacy.load(str(model_path / "model-best"))
    examples = []
    for doc, (_, label) in nlp_textcat.pipe(data, as_tuples=True):
        examples.append(
            Example.from_dict(
                doc, {"cats": {cat: 1 if cat == label else 0 for cat in cats}}
            )
        )

    scorer = Scorer(nlp_textcat)
    scores = scorer.score_cats(examples, "cats", labels=cats, multi_label=False)
    return scores


def batch_predict(model_path: Path, data: Dataset, is_train: bool) -> Records:
    nlp_textcat = spacy.load(str(model_path / "model-best"))
    predictions = []
    for doc, (_id, label) in nlp_textcat.pipe(data, as_tuples=True):
        predicted_cat = max(doc.cats, key=lambda x: doc.cats[x])
        predictions.append(
            {
                "id": _id,
                "pred": predicted_cat,
                "truth": label,
                "correct": label == predicted_cat,
                "confidence": doc.cats[predicted_cat],
                "is_train": is_train,
            }
        )
    return predictions


@op(
    ins={"start_after": In(Nothing)},
    out={"train": Out(Dataset), "valid": Out(Dataset), "cats": Out(Set[str])},
    required_resource_keys={"bigquery"},
)
def get_dataset(context):
    posts = bq.get_table_as_records(
        context.resources.bigquery, dataset="reddit_texts", table="posts_clean"
    )
    texts = []
    labels = []
    ids = []
    for post in posts:
        ids.append(post["id"])
        texts.append(post["text"])
        labels.append(post["subreddit"])

    cats = set(labels)
    # Split train and valid sets, keeping ids aligned
    X_train, X_valid, y_train, y_valid = train_test_split(
        list(zip(texts, ids)), labels, test_size=context.op_config["validation_split"]
    )
    text_train, ids_train = list(zip(*X_train))
    train_data = list(zip(text_train, zip(ids_train, y_train)))
    text_valid, ids_valid = list(zip(*X_valid))
    valid_data = list(zip(text_valid, zip(ids_valid, y_valid)))
    # print(train_data)
    # print(type(train_data), type(train_data[0]))
    # print(type(train_data[0][0]), type(train_data[0][1]), type(train_data[0][2]))
    yield Output(train_data, "train")
    yield Output(valid_data, "valid")
    yield Output(cats, "cats")


@op
def train_model(
    context, train_data: Dataset, valid_data: Dataset, cats: Set[str]
) -> Path:
    make_docs(train_data, ROOT_DIR / "tmp/train.spacy", cats)
    make_docs(valid_data, ROOT_DIR / "tmp/valid.spacy", cats)
    output_path = (
        ROOT_DIR
        / f"models/default_textcat/{datetime.date.today().strftime('%Y/%m/%d')}"
    )
    spacy_train(
        ROOT_DIR / "spacy_configs/subreddit_classif/default_textcat.cfg",
        output_path=output_path,
        overrides={
            "paths.train": str(ROOT_DIR / "tmp/train.spacy"),
            "paths.dev": str(ROOT_DIR / "tmp/valid.spacy"),
        },
    )
    return output_path


@op
def compute_model_perf(
    context,
    model_trained: Path,
    train_data: Dataset,
    valid_data: Dataset,
    cats: Set[str],
) -> Records:
    scores = {
        "train": stringify_nested(score_text_cat(model_trained, train_data, cats)),
        "valid": stringify_nested(score_text_cat(model_trained, valid_data, cats)),
    }
    return [
        {
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "model": "default_textcat",
            "type": name,
            **scores,
        }
        for name, score in scores.items()
    ]


@op(ins={"start_after": In(Nothing)})
def batch_predict_op(context, train_data: Dataset, valid_data: Dataset) -> Records:
    model_path = get_latest_model("default_textcat")
    return [
        *batch_predict(model_path, train_data, is_train=True),
        *batch_predict(model_path, train_data, is_train=False),
    ]


k_means_iris = dm.define_dagstermill_op(
    "plot_model_perfs",
    ROOT_DIR / "notebooks" / "prod" / "model_perfs.ipynb",
    output_notebook_name="model_perfs_out",
)


@job(resource_defs={"output_notebook_io_manager": dm.local_output_notebook_io_manager})
@graph(ins={"start_after": GraphIn()}, out=GraphOut())
def train_subreddit_graph(start_after):
    train_data, valid_data, cats = get_dataset(start_after)
    model_trained = train_model(train_data, valid_data, cats)
    scores = compute_model_perf(model_trained, train_data, valid_data, cats)
    bq.load_data.alias("load_model_perfs")(scores)
    predictions = batch_predict_op(train_data, valid_data, start_after=model_trained)
    return bq.load_data.alias("load_predictions")(predictions)


train_subreddit = train_subreddit_graph.to_job(
    resource_defs={
        "bigquery": bq.bigquery_resource,
        "output_notebook_io_manager": dm.local_output_notebook_io_manager,
    }
)


@job(resource_defs={"bigquery": bq.bigquery_resource})
def predict_subreddit():
    train_data, valid_data, _ = get_dataset()
    predictions = batch_predict_op(train_data, valid_data)
    bq.load_data.alias("load_predictions")(predictions)
