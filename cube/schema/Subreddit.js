cube(`Subreddit`, {
  sql: `SELECT * FROM reddit_predictions.subreddit`,

  preAggregations: {
    // Pre-Aggregations definitions go here
    // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
  },

  joins: {

  },

  measures: {
    count: {
      type: `count`,
      drillMembers: [confidence, id, modelDate]
    }
  },

  dimensions: {
    modelType: {
      sql: `model_type`,
      type: `string`
    },

    isTrain: {
      sql: `is_train`,
      type: `string`
    },

    model: {
      sql: `model`,
      type: `string`
    },

    confidence: {
      sql: `confidence`,
      type: `string`
    },

    truth: {
      sql: `truth`,
      type: `string`
    },

    correct: {
      sql: `correct`,
      type: `string`
    },

    pred: {
      sql: `pred`,
      type: `string`
    },

    id: {
      sql: `id`,
      type: `string`,
      primaryKey: true
    },

    modelDate: {
      sql: `model_date`,
      type: `time`
    }
  },

  dataSource: `default`
});
