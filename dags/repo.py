from dagster import ScheduleDefinition, repository

import jobs.reddit_elt as elt
import jobs.subreddit_prediction as spred

reddit_full_pipeline_schedule = ScheduleDefinition(
    job=elt.reddit_full_pipeline, cron_schedule="0 12 * * 0"
)

reddit_fcp_schedule = ScheduleDefinition(
    job=elt.reddit_fetch_clean_predict, cron_schedule="0 12 * * 1-6"
)

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
        elt.run_dbt_statistics,
        elt.run_text_prep,
        elt.run_text_prep_from_scratch,
    ]
