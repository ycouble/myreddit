from typing import Any, Dict, List

from dagster_gcp import bigquery_resource  # noqa
from google.cloud import bigquery

from dagster import op

Records = List[Dict[str, Any]]


@op(required_resource_keys={"bigquery"}, config_schema={"dataset": str, "table": str})
def load_data_in_bq(context, records: Records):
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
