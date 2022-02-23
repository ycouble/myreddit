import cubejs from '@cubejs-client/core';
import { QueryRenderer } from '@cubejs-client/react';
import { Spin } from 'antd';
import { makeStyles } from '@material-ui/styles';
import 'antd/dist/antd.css';
import React from 'react';
import { Line } from 'react-chartjs-2';
import { useDeepCompareMemo } from 'use-deep-compare';
import { Card, CardContent, CardHeader, Divider } from '@material-ui/core';

const COLORS_SERIES = [
    '#5b8ff9',
    '#5ad8a6',
    '#5e7092',
    '#f6bd18',
    '#6f5efa',
    '#6ec8ec',
    '#945fb9',
    '#ff9845',
    '#299796',
    '#fe99c3',
];
const commonOptions = {
    maintainAspectRatio: false,
    interaction: {
        intersect: false,
    },
    plugins: {
        legend: {
            position: 'bottom',
        },
    },
    scales: {
        x: {
            ticks: {
                autoSkip: true,
                maxRotation: 0,
                padding: 12,
                minRotation: 0,
            },
        },
    },
};
const useStyles = makeStyles(() => ({
    root: {},
    chartContainer: {
        position: 'relative',
        padding: '19px 0',
        minHeight: '20vw',
    },
}));

const useDrilldownCallback = ({
    datasets,
    labels,
    onDrilldownRequested,
    pivotConfig,
}) => {
    return React.useCallback(
        (elements) => {
            if (elements.length <= 0) return;
            const { datasetIndex, index } = elements[0];
            const { yValues } = datasets[datasetIndex];
            const xValues = [labels[index]];

            if (typeof onDrilldownRequested === 'function') {
                onDrilldownRequested(
                    {
                        xValues,
                        yValues,
                    },
                    pivotConfig
                );
            }
        },
        [datasets, labels, onDrilldownRequested]
    );
};

const LineChartRenderer = ({ resultSet, onDrilldownRequested }) => {
    const datasets = useDeepCompareMemo(
        () =>
            resultSet.series().map((s, index) => ({
                label: s.title,
                data: s.series.map((r) => r.value),
                yValues: [s.key],
                borderColor: COLORS_SERIES[index],
                pointRadius: 1,
                tension: 0.1,
                pointHoverRadius: 1,
                borderWidth: 2,
                tickWidth: 1,
                fill: false,
            })),
        [resultSet]
    );
    const data = {
        labels: resultSet.categories().map((c) => c.x),
        datasets,
    };
    const getElementAtEvent = useDrilldownCallback({
        datasets: data.datasets,
        labels: data.labels,
        onDrilldownRequested,
    });
    return (
        <Line
            type="line"
            data={data}
            options={commonOptions}
            getElementAtEvent={getElementAtEvent}
        />
    );
};


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

    return (
        <LineChartRenderer
            resultSet={resultSet}
        />
    );

};

const PostCumsums = () => {
    const classes = useStyles();
    return (
        <Card>
            <CardHeader title="Number of Unique Posts in DB per Subreddit" />
            <Divider />
            <CardContent>
                <div className={classes.chartContainer}>
                    <QueryRenderer
                        query={{
                            "measures": [
                                "PostCounts.cumsum_distinct"
                            ],
                            "timeDimensions": [
                                {
                                    "dimension": "PostCounts.fetchDate",
                                    "granularity": "day",
                                    "dateRange": [
                                        "2022-01-01",
                                        "2022-02-23"
                                    ]
                                }
                            ],
                            "order": {
                                "PostCounts.cumsum_distinct": "desc"
                            },
                            "filters": [],
                            "dimensions": [
                                "PostCounts.subreddit"
                            ]
                        }}
                        cubejsApi={cubejsApi}
                        resetResultSetOnChange={false}
                        render={(props) => renderChart({
                            ...props,
                            chartType: 'line',
                            pivotConfig: {
                                "x": [
                                    "PostCounts.fetchDate.day"
                                ],
                                "y": [
                                    "PostCounts.subreddit",
                                    "measures"
                                ],
                                "fillMissingDates": true,
                                "joinDateRange": false
                            }
                        })}
                    />
                </div>
            </CardContent>
        </Card>
    );
};

export default PostCumsums;
