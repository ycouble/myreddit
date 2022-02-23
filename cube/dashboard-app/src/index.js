import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import * as serviceWorker from './serviceWorker';
import { HashRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import DataTablePage from './pages/DataTablePage';
import IFramePage from './pages/IFramePage';
import UsersPage from './pages/UsersPage';

ReactDOM.render(
  <React.StrictMode>
    <Router>
      <App>
        <Switch>
          <Redirect exact from="/" to="/dashboard" />
          <Route key="index" exact path="/dashboard" component={DashboardPage} />
          <Route key="table" path="/dagit" render={(props) => <IFramePage url="http://localhost:3500" />} />
          <Route key="table" path="/rubrix" render={(props) => <IFramePage url="http://localhost:6900" />} />
          <Route key="table" path="/apps" render={(props) => <IFramePage url="http://localhost:8501" />} />
          <Route key="table" path="/app_spacy" render={(props) => <IFramePage url="http://localhost:8502" />} />
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
