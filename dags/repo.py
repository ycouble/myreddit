import yaml
from dagster import ScheduleDefinition, repository, schedule

import jobs.reddit_elt as elt
import jobs.subreddit_prediction as spred
from jobs.definitions import ROOT_DIR

config_folder = ROOT_DIR / "dags" / "jobs" / "configs"
schedule_kwargs = {
    "execution_timezone": "Europe/Paris",
}


def read_config(name: str) -> dict:
    with open(config_folder / name, "r") as stream:
        return yaml.safe_load(stream)


@schedule(
    cron_schedule="0 10 * * 0",
    job=elt.reddit_full_pipeline,
    **schedule_kwargs,
)
def reddit_full_pipeline_schedule(context):
    return read_config("reddit_elt.yml")


reddit_fcp_schedule = ScheduleDefinition(
    job=elt.reddit_fetch_clean_predict, cron_schedule="0 10 * * 1-6", **schedule_kwargs
)


def reddit_fcp_schedule(context):
    return read_config("reddit_fcp.yml")


@schedule(
    cron_schedule="22 11 * * 1-6",
    job=elt.reddit_fetch_clean_predict,
    **schedule_kwargs,
)
def reddit_fcp_schedule(context):
    return read_config("reddit_fcp.yml")


# @sensor(job=job2)
# def job2_sensor():
#     should_run = True
#     if should_run:
#         yield RunRequest(run_key=None, run_config={})


@repository
def my_repository():
    return [
        reddit_fcp_schedule,
        reddit_full_pipeline_schedule,
        spred.train_subreddit,
        spred.predict_subreddit,
        spred.run_model_perfs_nb,
        spred.populate_rubrix,
        elt.run_dbt_statistics,
        elt.run_text_prep,
        elt.run_text_prep_from_scratch,
    ]
