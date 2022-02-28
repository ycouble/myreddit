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
          <Route key="table" path="/pipelines" render={(props) => <IFramePage url={process.env('REACT_APP_DOMAIN') + "/zpipelines"} />} />
          <Route key="table" path="/rubrix" render={(props) => <IFramePage url={process.env('REACT_APP_DOMAIN') + "/zrubrix/"} />} />
          <Route key="table" path="/apps" render={(props) => <IFramePage url={process.env('REACT_APP_DOMAIN') + "/zapps"} />} />
          <Route key="table" path="/app_spacy" render={(props) => <IFramePage url={process.env('REACT_APP_DOMAIN') + "/zapp_spacy"} />} />
          <Route key="table" path="/cubejs" render={(props) => <IFramePage url={process.env('REACT_APP_DOMAIN') + "/zcubejs"} />} />
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
