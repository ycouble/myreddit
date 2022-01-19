from dagster import ScheduleDefinition, repository

import jobs.reddit_elt as elt

fetch_schedule = ScheduleDefinition(
    job=elt.reddit_full_pipeline, cron_schedule="0 12 * * *"
)

# @sensor(job=job2)
# def job2_sensor():
#     should_run = True
#     if should_run:
#         yield RunRequest(run_key=None, run_config={})


@repository
def my_repository():
    return [
        fetch_schedule,
        elt.run_dbt_statistics,
        elt.run_text_prep,
        elt.run_text_prep_from_scratch,
        # job2_sensor,
    ]
