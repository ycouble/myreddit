from jobs.fetch_subreddits import reddit_extract_load, run_dbt_statistics

from dagster import ScheduleDefinition, repository

fetch_schedule = ScheduleDefinition(job=reddit_extract_load, cron_schedule="0 12 * * *")

# @sensor(job=job2)
# def job2_sensor():
#     should_run = True
#     if should_run:
#         yield RunRequest(run_key=None, run_config={})


@repository
def my_repository():
    return [
        fetch_schedule,
        run_dbt_statistics,
        # job2_sensor,
    ]
