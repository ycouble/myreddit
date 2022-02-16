from typing import Any, Dict, List, Optional

from dagster import Field, op, resource
from google.cloud import bigquery
from google.oauth2 import service_account

from jobs.common.types import Records


@resource(description="Dagster resource for connecting to BigQuery")
def bigquery_resource(context):
    key_path = "/opt/dagster/gcp_key.json"
    credentials = service_account.Credentials.from_service_account_file(key_path)

    return bigquery.Client(
        credentials=credentials,
        project=credentials.project_id,
    )


def table_exists(bq_client: bigquery.Client, dataset: str, table: str):
    return table in (t.table_id for t in bq_client.list_tables(dataset))


def drop_table(bq_client: bigquery.Client, dataset: str, table: str):
    bq_client.delete_table(f"{dataset}.{table}")


def get_table_as_records(
    bq_client: bigquery.Client,
    dataset: str,
    table: str,
    where_clause: Optional[str] = None,
) -> Records:
    query_job = bq_client.query(
        f"SELECT * FROM `{dataset}.{table}` "
        f"{'WHERE ' + where_clause if where_clause else ''};"
    )
    return [dict(row) for row in query_job]


@op(
    required_resource_keys={"bigquery"},
    config_schema={
        "dataset": str,
        "table": str,
        "drop_if_exist": Field(bool, default_value=False),
    },
)
def load_data(context, records: Records):
    dataset, table = context.op_config["dataset"], context.op_config["table"]
    table_ref = f"{dataset}.{table}"
    job_config = bigquery.LoadJobConfig()
    if context.op_config["drop_if_exist"]:
        context.resources.bigquery.delete_table(table_ref)
    if table_exists(context.resources.bigquery, dataset, table):
        job_config.autodetect = False
        job_config.schema = context.resources.bigquery.get_table(table_ref).schema
        schema_fields = [f.name for f in job_config.schema]
        for record in records:
            for field in list(record.keys()):
                if field not in schema_fields:
                    record.pop(field)
    else:
        job_config.autodetect = True
    job_config.schema_update_options = [
        "ALLOW_FIELD_ADDITION",
        "ALLOW_FIELD_RELAXATION",
    ]
    job_config.write_disposition = "WRITE_APPEND"
    context.resources.bigquery.load_table_from_json(
        records, table_ref, job_config=job_config
    ).result()
