select
    subreddit,
    count(id) as posts,
    sum(num_comments) as total_comments,
    sum(ups) as total_ups,
    sum(downs) as total_downs,
from {{ ref('posts') }}
group by subreddit
