cube(`Posts`, {
  sql: `SELECT * FROM reddit_statistics.posts`,

  preAggregations: {
    // Pre-Aggregations definitions go here
    // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
  },

  joins: {

  },

  measures: {
    count: {
      type: `count`,
      drillMembers: [id, creationDate, fetchDate]
    }
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

    numReports: {
      sql: `num_reports`,
      type: `string`
    },

    viewCount: {
      sql: `view_count`,
      type: `string`
    },

    visited: {
      sql: `visited`,
      type: `string`
    },

    creationDate: {
      sql: `creation_date`,
      type: `string`
    },

    fetchDate: {
      sql: `fetch_date`,
      type: `time`
    }
  },

  dataSource: `default`
});
