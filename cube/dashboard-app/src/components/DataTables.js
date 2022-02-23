import cubejs from '@cubejs-client/core';
import { QueryRenderer } from '@cubejs-client/react';
import { Spin } from 'antd';
import 'antd/dist/antd.css';
import React from 'react';
import { useDeepCompareMemo } from 'use-deep-compare';
import { Table } from 'antd';
import { Card, CardContent, CardHeader, Divider } from '@material-ui/core';

const formatTableData = (columns, data) => {
  function flatten(columns = []) {
    return columns.reduce((memo, column) => {
      if (column.children) {
        return [...memo, ...flatten(column.children)];
      }

      return [...memo, column];
    }, []);
  }

  const typeByIndex = flatten(columns).reduce((memo, column) => {
    return { ...memo, [column.dataIndex]: column };
  }, {});

  function formatValue(value, { type, format } = {}) {
    if (value === undefined) {
      return value;
    }

    if (type === 'boolean') {
      if (typeof value === 'boolean') {
        return value.toString();
      } else if (typeof value === 'number') {
        return Boolean(value).toString();
      }

      return value;
    }

    if (type === 'number' && format === 'percent') {
      return [parseFloat(value).toFixed(2), '%'].join('');
    }

    return value.toString();
  }

  function format(row) {
    return Object.fromEntries(
      Object.entries(row).map(([dataIndex, value]) => {
        return [dataIndex, formatValue(value, typeByIndex[dataIndex])];
      })
    );
  }

  return data.map(format);
};

const TableRenderer = ({ resultSet, pivotConfig }) => {
  const [tableColumns, dataSource] = useDeepCompareMemo(() => {
    const columns = resultSet.tableColumns(pivotConfig);
    return [
      columns,
      formatTableData(columns, resultSet.tablePivot(pivotConfig)),
    ];
  }, [resultSet, pivotConfig]);
  return (
    <Table pagination={false} columns={tableColumns} dataSource={dataSource} />
  );
};

// FIXME:
const cubejsApi = cubejs(
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NDU2MDYwNDcsImV4cCI6MTY0NTY5MjQ0N30.eRuVB9M9M9WaiaBgXkUVo0Z7pl2gl3kydoa0MgQN2AQ',
  { apiUrl: 'http://localhost:4000/cubejs-api/v1' }
);

const renderChart = ({ resultSet, error, pivotConfig }) => {
  if (error) {
    return <div>{error.toString()}</div>;
  }

  if (!resultSet) {
    return <Spin />;
  }

  return <TableRenderer resultSet={resultSet} pivotConfig={pivotConfig} />;

};

const PostStats = () => {
  return (

    <Card>
      <CardHeader title="Subreddit Posts Statistics" />
      <Divider />
      <CardContent>
        <QueryRenderer
          query={{
            "measures": [
              "PostStats.count",
              "PostStats.ups_per_post",
              "PostStats.downs_per_post",
              "PostStats.nb_comments_per_post"
            ],
            "timeDimensions": [
              {
                "dimension": "PostStats.fetchDate"
              }
            ],
            "order": {
              "PostStats.count": "desc"
            },
            "dimensions": [
              "PostStats.subreddit"
            ]
          }}
          cubejsApi={cubejsApi}
          resetResultSetOnChange={false}
          render={(props) => renderChart({
            ...props,
            chartType: 'table',
            pivotConfig: {
              "x": [
                "PostStats.subreddit"
              ],
              "y": [
                "measures"
              ],
              "fillMissingDates": true,
              "joinDateRange": false
            }
          })}
        />
      </CardContent>
    </Card>
  );
};


const CommentStats = () => {
  return (

    <Card>
      <CardHeader title="Subreddit Comments Statistics" />
      <Divider />
      <CardContent>
        <QueryRenderer
          query={{
            "measures": [
              "CommentStats.count",
              "CommentStats.nb_ups_per_comment",
              "CommentStats.downs_per_comment",
              "CommentStats.average_comment_depth"
            ],
            "timeDimensions": [
              {
                "dimension": "CommentStats.fetchDate"
              }
            ],
            "order": {
              "CommentStats.count": "desc"
            },
            "dimensions": [
              "CommentStats.subreddit"
            ]
          }}
          cubejsApi={cubejsApi}
          resetResultSetOnChange={false}
          render={(props) => renderChart({
            ...props,
            chartType: 'table',
            pivotConfig: {
              "x": [
                "CommentStats.subreddit"
              ],
              "y": [
                "measures"
              ],
              "fillMissingDates": true,
              "joinDateRange": false
            }
          })}
        />
      </CardContent>
    </Card>
  );
};





export { PostStats, CommentStats };
