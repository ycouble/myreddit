import datetime
from typing import Any, Dict, List

import requests
from dagster import ModeDefinition, job, make_values_resource, op
from dagster_gcp import bigquery_resource
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

Records = List[Dict[str, Any]]


MY_SUBREDDITS = ["dataengineering", "datasets", "LanguageTechnology"]


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
        print(subreddit)
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


@op(required_resource_keys={"bigquery"}, config_schema={"dataset": str, "table": str})
def load_data_in_bq(context, records: Records):
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.schema_update_options = [
        "ALLOW_FIELD_ADDITION",
        "ALLOW_FIELD_RELAXATION",
    ]
    job_config.write_disposition = "WRITE_APPEND"
    # job_config.source_format = "CSV"
    context.resources.bigquery.load_table_from_json(
        records,
        f"{context.op_config['dataset']}.{context.op_config['table']}",
        job_config=job_config,
    ).result()


@job(
    resource_defs={
        "reddit": make_values_resource(
            app_id=str,
            secret=str,
            username=str,
            password=str,
            posts_limit=int,
            comments_limit=int,
            comments_depth=int,
        ),
        "bigquery": bigquery_resource,
    }
)
def reddit_extract_load():

    post_records = extract_posts()
    comment_records = extract_comments(post_records)
    # import_df_to_bq.alias("import_posts_to_bq")(df_posts)
    load_data_in_bq.alias("import_posts_to_bq")(post_records)
    load_data_in_bq.alias("import_comments_to_bq")(comment_records)
