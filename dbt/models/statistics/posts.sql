with from_posts as (
    select
        id,
        subreddit,
        link_flair_text as tag,
        fetch_date,
        num_comments,
        num_reports,
        ups,
        downs,
        view_count,
        visited,
        created_utc as creation_date
    from {{ source('raw', 'posts') }}
)

select * from from_posts
