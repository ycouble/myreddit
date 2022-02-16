import datetime

import dagstermill as dm
import requests
from dagster import (
    GraphOut,
    In,
    Nothing,
    Out,
    Output,
    graph,
    job,
    make_values_resource,
    op,
)
from dagster_dbt import dbt_cli_resource

import jobs.common.bigquery as bq
import jobs.common.text_prep as text_prep
from jobs.common.types import Records
from jobs.subreddit_prediction import (
    batch_predict_graph,
    get_dataset,
    train_subreddit_graph,
)

# Resources
dbt_resource = dbt_cli_resource.configured(
    {"project_dir": "/opt/dagster/dbt/", "profiles_dir": "/opt/dagster/dbt/profiles"}
)

REDDIT_ELT_RESOURCES = {
    "reddit": make_values_resource(
        app_id=str,
        secret=str,
        username=str,
        password=str,
        posts_limit=int,
        comments_limit=int,
        comments_depth=int,
    ),
    "bigquery": bq.bigquery_resource,
    "dbt": dbt_resource,
    "output_notebook_io_manager": dm.local_output_notebook_io_manager,
}

MY_SUBREDDITS = [
    "dataengineering",
    "datasets",
    "LanguageTechnology",
    "deeplearning",
    "datascience",
    "statistics",
]


def filter_nested(data):
    data = data.copy()
    return {
        k: v
        for k, v in data.items()
        if not isinstance(v, dict)
        and not isinstance(v, list)
        and not isinstance(v, set)
    }


def login_headers(context):
    auth = requests.auth.HTTPBasicAuth(
        context.resources.reddit["app_id"], context.resources.reddit["secret"]
    )
    login_data = {
        "grant_type": "password",
        "username": context.resources.reddit["username"],
        "password": context.resources.reddit["password"],
    }
    login_headers = {"User-Agent": "MySubrs"}
    res = requests.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=login_data,
        headers=login_headers,
    )
    token = res.json()["access_token"]
    return {**login_headers, **{"Authorization": f"bearer {token}"}}


@op(required_resource_keys={"reddit"})
def extract_posts(context) -> Records:
    headers = login_headers(context)
    date = datetime.date.today()
    raw_data = []
    for subreddit in MY_SUBREDDITS:
        context.log.info(subreddit)
        resp = requests.get(
            f"https://oauth.reddit.com/r/{subreddit}/hot"
            f"?limit={context.resources.reddit['posts_limit']}",
            headers=headers,
        ).json()
        for article in resp["data"]["children"]:
            article = {
                k: v
                for k, v in article["data"].items()
                if not isinstance(v, dict) and not isinstance(v, list)
            }
            raw_data.append(
                {
                    "fetch_date": date.strftime("%Y-%m-%d"),
                    "subreddit": subreddit,
                    **article,
                }
            )

    return raw_data


@op(required_resource_keys={"reddit"})
def extract_comments(context, post_records: Records) -> Records:
    headers = login_headers(context)
    date = datetime.date.today().strftime("%Y-%m-%d")
    comments_data = []

    def rec_add_comment(tree, subreddit):
        if tree.get("replies", "") == "":
            return
        for child in tree["replies"]["data"]["children"]:
            child_data = {
                **filter_nested(child["data"]),
                "fetch_date": date,
                "subreddit": subreddit,
            }
            comments_data.append(child_data)
            rec_add_comment(child["data"], subreddit)

    for row in post_records:
        post_id = row["id"]
        subreddit = row["subreddit"]
        comment_data = requests.get(
            f"https://oauth.reddit.com/r/{subreddit}/comments/{post_id}"
            f"?limit={context.resources.reddit['comments_limit']}"
            f"&depth={context.resources.reddit['comments_depth']}",
            headers=headers,
        ).json()
        comment_trees = comment_data[1]["data"]["children"]
        for tree in comment_trees:
            rec_add_comment(tree["data"], subreddit)

    return comments_data


@op(required_resource_keys={"dbt"}, ins={"start_after": In(Nothing)})
def run_dbt_transformations(context):
    context.resources.dbt.run(models=["tag:ingestion"])


@op(
    required_resource_keys={"bigquery"},
    ins={"start_after": In(Nothing)},
    out={"posts": Out(Records)},
)
def get_raw_texts(context):
    if bq.table_exists(
        context.resources.bigquery, dataset="reddit_texts", table="posts_clean"
    ):
        where_clause_posts = "id NOT IN (SELECT id from `reddit_texts.posts_clean`)"
    else:
        where_clause_posts = None
    yield Output(
        bq.get_table_as_records(
            context.resources.bigquery,
            dataset="reddit_texts",
            table="post_contents",
            where_clause=where_clause_posts,
        ),
        "posts",
    )


@op()
def posts_text_cleaning(posts: Records) -> Records:
    return [
        text_prep.preprocess(post, field="selftext", new_field="text") for post in posts
    ]


@op(required_resource_keys={"bigquery"})
def drop_clean_tables(context):
    clean_tables = {"reddit_texts": ["posts_clean"]}
    for dataset, tables in clean_tables.items():
        for table in tables:
            bq.drop_table(context.resources.bigquery, dataset, table)


@graph(out=GraphOut())
def preprocess_texts(start_after):
    posts = get_raw_texts(start_after)
    return bq.load_data.alias("load_clean_texts")(posts_text_cleaning(posts))


@graph
def reddit_el():
    post_records = extract_posts()
    comment_records = extract_comments(post_records)
    bq.load_data.alias("import_posts_to_bq")(post_records)
    return bq.load_data.alias("import_comments_to_bq")(comment_records)


@job(resource_defs=REDDIT_ELT_RESOURCES)
def reddit_fetch_clean_predict():
    el_done = reddit_el()
    dbt_done = run_dbt_transformations(start_after=el_done)
    prep_done = preprocess_texts(start_after=dbt_done)
    train_data, valid_data, _ = get_dataset(start_after=prep_done)
    batch_predict_graph(train_data, valid_data, start_after=prep_done)


@job(resource_defs=REDDIT_ELT_RESOURCES)
def reddit_full_pipeline():
    el_done = reddit_el()
    dbt_done = run_dbt_transformations(start_after=el_done)
    prep_done = preprocess_texts(start_after=dbt_done)
    train_subreddit_graph(start_after=prep_done)


@job(resource_defs={"dbt": dbt_resource})
def run_dbt_statistics():
    run_dbt_transformations()


@job(resource_defs={"bigquery": bq.bigquery_resource})
def run_text_prep():
    preprocess_texts()


@job(resource_defs={"bigquery": bq.bigquery_resource})
def run_text_prep_from_scratch():
    drop_done = drop_clean_tables()
    preprocess_texts(start_after=drop_done)
