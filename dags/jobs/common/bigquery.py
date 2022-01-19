from typing import Any, Dict, List, Optional

from dagster import op
from dagster_gcp import bigquery_resource  # noqa
from google.cloud import bigquery

Records = List[Dict[str, Any]]


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


@op(required_resource_keys={"bigquery"}, config_schema={"dataset": str, "table": str})
def load_data(context, records: Records):
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.schema_update_options = [
        "ALLOW_FIELD_ADDITION",
        "ALLOW_FIELD_RELAXATION",
    ]
    job_config.write_disposition = "WRITE_APPEND"
    context.resources.bigquery.load_table_from_json(
        records,
        f"{context.op_config['dataset']}.{context.op_config['table']}",
        job_config=job_config,
    ).result()
