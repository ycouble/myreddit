import React from 'react';
import { Grid } from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';
import { PostStats, CommentStats } from '../components/DataTables';
import PostCumsums from '../components/PostCumsums.js';

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(4),
  },
}));

const Dashboard = () => {
  const classes = useStyles();
  return (
    <div className={classes.root}>
      <Grid container spacing={4}>
        {/* {cards.map((item, index) => {
          return (
            <Grid key={item.title + index} item lg={3} sm={6} xl={3} xs={12}>
              <KPIChart {...item} />
            </Grid>
          );
        })} */}
        <Grid item lg={12} md={12} xl={6} xs={12}>
          <PostStats />
        </Grid>
        <Grid item lg={12} md={12} xl={6} xs={12}>
          <CommentStats />
        </Grid>
        <Grid item lg={12} md={12} xl={12} xs={12}>
          <PostCumsums />
        </Grid>
      </Grid>
    </div>
  );
};

export default Dashboard;
