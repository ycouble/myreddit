cube(`CommentStats`, {
    sql: `SELECT * FROM reddit_statistics.comments`,

    preAggregations: {
        // Pre-Aggregations definitions go here
        // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
    },

    joins: {

    },

    measures: {
        count: {
            sql: `link_id`,
            type: `countDistinct`,
            drillMembers: [link_id, subreddit]
        },
        nb_ups_per_comment: {
            sql: `ups`,
            type: `avg`,
        },
        downs_per_comment: {
            sql: `downs`,
            type: `avg`,
        },
        average_comment_depth: {
            sql: `depth`,
            type: `avg`,
        },
    },

    dimensions: {
        link_id: {
            sql: `link_id`,
            type: `string`,
            primaryKey: true
        },

        subreddit: {
            sql: `subreddit`,
            type: `string`
        },

        fetchDate: {
            sql: `timestamp(fetch_date)`,
            type: `time`
        }
    },

    dataSource: `default`
});
