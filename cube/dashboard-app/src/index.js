import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import * as serviceWorker from './serviceWorker';
import { HashRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import IFramePage from './pages/IFramePage';
import UsersPage from './pages/UsersPage';

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <App>
        <Switch>
          <Redirect exact from="/" to="/dashboard" />
          <Route key="index" exact path="/dashboard" component={DashboardPage} />
          <Route key="table" path="/pipelines" render={(props) => <IFramePage url={"http://dagit." + process.env.REACT_APP_DOMAIN} />} />
          <Route key="table" path="/rubrix" render={(props) => <IFramePage url={"http://rubrix." + process.env.REACT_APP_DOMAIN} />} />
          <Route key="table" path="/apps" render={(props) => <IFramePage url={"http://apps." + process.env.REACT_APP_DOMAIN} />} />
          <Route key="table" path="/app_spacy" render={(props) => <IFramePage url={"http://spacy_app." + process.env.REACT_APP_DOMAIN} />} />
          <Route key="table" path="/cubejs" render={(props) => <IFramePage url={"http://cube." + process.env.REACT_APP_DOMAIN} />} />
          <Route key="table" path="/user/:id" component={UsersPage} />
          <Redirect to="/dashboard" />
        </Switch>
      </App>
    </Router>
  </React.StrictMode>,
  document.getElementById('root')
); // If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA

serviceWorker.unregister();
