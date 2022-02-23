cube(`PostCounts`, {
    sql: `SELECT fetch_date, subreddit, tag, count(*) as count, count(distinct(id)) as count_distinct FROM reddit_statistics.posts GROUP BY subreddit, tag, fetch_date`,

    preAggregations: {
        // Pre-Aggregations definitions go here
        // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
    },

    joins: {

    },

    measures: {
        cumsum: {
            sql: `count`,
            type: `runningTotal`,
        },
        cumsum_distinct: {
            sql: `count_distinct`,
            type: `runningTotal`,
        },
    },

    dimensions: {

        subreddit: {
            sql: `subreddit`,
            type: `string`
        },

        tag: {
            sql: `tag`,
            type: `string`
        },

        fetchDate: {
            sql: `timestamp(fetch_date)`,
            type: `time`
        }
    },

    dataSource: `default`
});
