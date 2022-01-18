select
    distinct(id),
    subreddit,
    link_flair_text as tag,
    selftext,
from {{ source('raw', 'posts') }}
where length(selftext) > 0
