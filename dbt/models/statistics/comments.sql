with from_comments as (
    select
        link_id,
        parent_id,
        depth,
        subreddit,
        fetch_date,
        ups,
        downs,
        is_submitter,
    from {{ source('raw', 'comments') }}
)

select * from from_comments
