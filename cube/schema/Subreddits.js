cube(`Subreddits`, {
  sql: `SELECT * FROM reddit_statistics.subreddits`,

  preAggregations: {
    // Pre-Aggregations definitions go here
    // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
  },

  joins: {

  },

  measures: {
    count: {
      type: `count`,
      drillMembers: []
    }
  },

  dimensions: {
    subreddit: {
      sql: `subreddit`,
      type: `string`
    }
  },

  dataSource: `default`
});
