cube(`Textcat`, {
  sql: `SELECT * FROM model_perfs.textcat`,

  preAggregations: {
    // Pre-Aggregations definitions go here
    // Learn more here: https://cube.dev/docs/caching/pre-aggregations/getting-started
  },

  joins: {

  },

  measures: {
    count: {
      type: `count`,
      drillMembers: [date]
    }
  },

  dimensions: {
    catsFPerType: {
      sql: `cats_f_per_type`,
      type: `string`
    },

    catsMacroAuc: {
      sql: `cats_macro_auc`,
      type: `string`
    },

    catsMacroF: {
      sql: `cats_macro_f`,
      type: `string`
    },

    catsMacroR: {
      sql: `cats_macro_r`,
      type: `string`
    },

    catsMicroF: {
      sql: `cats_micro_f`,
      type: `string`
    },

    catsScoreDesc: {
      sql: `cats_score_desc`,
      type: `string`
    },

    catsScore: {
      sql: `cats_score`,
      type: `string`
    },

    catsMicroR: {
      sql: `cats_micro_r`,
      type: `string`
    },

    model: {
      sql: `model`,
      type: `string`
    },

    catsMacroP: {
      sql: `cats_macro_p`,
      type: `string`
    },

    catsMicroP: {
      sql: `cats_micro_p`,
      type: `string`
    },

    catsAucPerType: {
      sql: `cats_auc_per_type`,
      type: `string`
    },

    modelType: {
      sql: `model_type`,
      type: `string`
    },

    type: {
      sql: `type`,
      type: `string`
    },

    date: {
      sql: `date`,
      type: `time`
    }
  },

  dataSource: `default`
});
