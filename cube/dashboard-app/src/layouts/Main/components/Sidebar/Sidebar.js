import React from 'react';
import clsx from 'clsx';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/styles';
import { Divider, Drawer } from '@material-ui/core';
import DashboardIcon from '@material-ui/icons/Dashboard';
import PageviewIcon from '@material-ui/icons/Pageview';
import SyncIcon from '@material-ui/icons/Sync';
import InsertChartIcon from '@material-ui/icons/InsertChart';
import DescriptionIcon from '@material-ui/icons/Description';
import BuildIcon from '@material-ui/icons/Build';

import { Profile, SidebarNav } from './components';

const useStyles = makeStyles((theme) => ({
  drawer: {
    width: 240,
    [theme.breakpoints.up('lg')]: {
      marginTop: 64,
      height: 'calc(100% - 64px)',
    },
  },
  root: {
    backgroundColor: theme.palette.white,
    display: 'flex',
    flexDirection: 'column',
    height: '100%',
    padding: theme.spacing(4),
  },
  divider: {
    margin: theme.spacing(4, 0, 1),
  },
  nav: {
    marginBottom: theme.spacing(2),
  },
}));

const Sidebar = (props) => {
  const { open, variant, onClose, className, ...rest } = props;

  const classes = useStyles();

  const pages = [
    {
      title: 'Dashboard',
      href: '/dashboard',
      icon: <DashboardIcon />,
    },
    {
      title: 'Apps',
      href: '/apps',
      icon: <InsertChartIcon />,
    },
    {
      title: 'Spacy Demo',
      href: '/app_spacy',
      icon: <DescriptionIcon />,
    },
    {
      title: 'Dashboard Builder',
      href: '/cubejs',
      icon: <BuildIcon />,
    },
    {
      title: 'Data Pipelines',
      href: '/pipelines',
      icon: <SyncIcon />,
    },
    {
      title: 'MLOps',
      href: '/rubrix',
      icon: <PageviewIcon />,
    },
  ];

  return (
    <Drawer anchor="left" classes={{ paper: classes.drawer }} onClose={onClose} open={open} variant={variant}>
      <div {...rest} className={clsx(classes.root, className)}>
        <Profile />
        <Divider className={classes.divider} />
        <SidebarNav className={classes.nav} pages={pages} />
      </div>
    </Drawer>
  );
};

Sidebar.propTypes = {
  className: PropTypes.string,
  onClose: PropTypes.func,
  open: PropTypes.bool.isRequired,
  variant: PropTypes.string.isRequired,
};

export default Sidebar;
