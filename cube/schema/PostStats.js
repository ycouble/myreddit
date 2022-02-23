cube(`PostStats`, {
  sql: `SELECT * FROM reddit_statistics.posts`,

  preAggregations: {
    // Pre-Aggregations definitions go here
    // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
  },

  joins: {

  },

  measures: {
    count: {
      sql: `id`,
      type: `countDistinct`,
      drillMembers: [id, subreddit, tag]
    },
    ups_per_post: {
      sql: `ups`,
      type: `avg`,
    },
    downs_per_post: {
      sql: `downs`,
      type: `avg`,
    },
    nb_comments_per_post: {
      sql: `num_comments`,
      type: `avg`,
    },
  },

  dimensions: {
    id: {
      sql: `id`,
      type: `string`,
      primaryKey: true
    },

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
