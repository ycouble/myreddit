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

SELECTED_MODEL = "textcat_ens"
nlp = spacy.load("en_core_web_md")

Dataset = List[Tuple[str, Tuple[str, str]]]


def prefix_dict(d: dict, prefix: str):
    return {f"{prefix}_{k}": v for k, v in d.items()}


def sanitize(d):
    return {
        k: str(v)
        if isinstance(v, dict)
        else v.strftime("%Y-%m-%d")
        if k == "date"
        else v
        for k, v in d.items()
    }


def get_latest_model(config: Path) -> Path:
    model_type = config.parent.name
    config_name = config.stem

    model_folder = ROOT_DIR / "models" / model_type / config_name
    for _ in ["year", "month", "day"]:
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


def batch_predict(
    config: Path, model_path: Path, data: Dataset, is_train: bool
) -> Records:
    model = config.stem
    model_type = config.parent.name
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
                "model": model,
                "model_type": model_type,
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


def op_factory_train_model(config: Path):
    model_type = config.parent.name
    config_name = config.stem
    config_path = str(config)

    @op(
        name=f"train_model_{config.stem}",
    )
    def train_model(
        context, train_data: Dataset, valid_data: Dataset, cats: Set[str]
    ) -> Path:
        make_docs(train_data, ROOT_DIR / "tmp/train.spacy", cats)
        make_docs(valid_data, ROOT_DIR / "tmp/valid.spacy", cats)
        model_path = (
            ROOT_DIR
            / f"models/{model_type}/{config_name}"
            / f"{datetime.date.today().strftime('%Y/%m/%d')}"
        )
        spacy_train(
            config_path,
            output_path=model_path,
            overrides={
                "paths.train": str(ROOT_DIR / "tmp/train.spacy"),
                "paths.dev": str(ROOT_DIR / "tmp/valid.spacy"),
            },
        )
        return model_path

    return train_model


@op
def compute_model_perf(
    context,
    model_trained: Path,
    train_data: Dataset,
    valid_data: Dataset,
    cats: Set[str],
) -> Records:
    model_dir_path = model_trained.parent.parent.parent
    model_name = model_dir_path.stem
    model_type = model_dir_path.parent.stem
    scores = {
        "train": sanitize(score_text_cat(model_trained, train_data, cats)),
        "valid": sanitize(score_text_cat(model_trained, valid_data, cats)),
    }
    return [
        {
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "model_type": model_type,
            "model": model_name,
            "type": name,
            **score,
        }
        for name, score in scores.items()
    ]


def op_factory_batch_predict(config: Path):
    @op(name=f"batch_predict_{config.stem}", ins={"start_after": In(Nothing)})
    def batch_predict_op(context, train_data: Dataset, valid_data: Dataset) -> Records:
        model_path = get_latest_model(config)
        return [
            *batch_predict(config, model_path, train_data, is_train=True),
            *batch_predict(config, model_path, valid_data, is_train=False),
        ]

    return batch_predict_op


run_perf_notebook = dm.define_dagstermill_op(
    "plot_model_perfs",
    str(ROOT_DIR / "notebooks" / "prod" / "model_perfs.ipynb"),
    output_notebook_name="model_perfs_out",
)


def graph_factory_batch_predict(config: Path):
    @graph(
        name=f"batch_predict_graph_{config.stem}",
        ins={
            "train_data": GraphIn(),
            "valid_data": GraphIn(),
            "start_after": GraphIn(),
        },
        out=GraphOut(),
    )
    def batch_predict_graph(train_data: Dataset, valid_data: Dataset, start_after):
        batch_predict_op = op_factory_batch_predict(config)
        predictions = batch_predict_op(train_data, valid_data, start_after=start_after)
        return bq.load_data.alias("load_predictions")(predictions)

    return batch_predict_graph


batch_predict_graph = graph_factory_batch_predict(
    ROOT_DIR / "spacy_configs" / "subreddit_classif" / f"{SELECTED_MODEL}.cfg"
)


@graph(ins={"start_after": GraphIn()}, out=GraphOut())
def train_subreddit_graph(start_after):
    model_type = "subreddit_classif"
    config_folder_path = ROOT_DIR / "spacy_configs" / model_type

    train_data, valid_data, cats = get_dataset(start_after)
    loaded = {}
    for config in config_folder_path.glob("*.cfg"):
        train_model = op_factory_train_model(config)
        model_trained = train_model(train_data, valid_data, cats)
        scores = compute_model_perf(model_trained, train_data, valid_data, cats)
        loaded[config.stem] = bq.load_data.alias(f"load_model_perfs_{config.stem}")(
            scores
        )

    return batch_predict_graph(
        train_data, valid_data, start_after=loaded[SELECTED_MODEL]
    )


train_subreddit = train_subreddit_graph.to_job(
    name="train_subreddit",
    resource_defs={
        "bigquery": bq.bigquery_resource,
        "output_notebook_io_manager": dm.local_output_notebook_io_manager,
    },
)


@job(resource_defs={"bigquery": bq.bigquery_resource})
def predict_subreddit():
    train_data, valid_data, _ = get_dataset()
    batch_predict_graph(train_data, valid_data)


@job(resource_defs={"output_notebook_io_manager": dm.local_output_notebook_io_manager})
def run_model_perfs_nb():
    run_perf_notebook()
