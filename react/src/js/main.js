import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRedirect, IndexRoute, hashHistory } from 'react-router';
import AuthService from '../utils/AuthService'
import Login from './pages/Login';
import Container from './pages/Container'

import Layout from './pages/Layout';
import Games from './pages/Games';
import Home from './pages/Home';
import Players from './pages/Players';
import Stats from './pages/Stats';
import Teams from './pages/Teams';
import TopStories from './pages/TopStories';

const app = document.getElementById('app');
const auth = new AuthService('sf4rjPzNoQe12MgSDhqZSwRtd9PyBKXd', 'andersonhuang.auth0.com');

const requireAuth = (nextState, replace) => {
  if (!auth.loggedIn()) {
    replace({ pathname: '/teams' })
  }
}

ReactDOM.render(
  <Router history={hashHistory}>
    <Route path="/" auth={auth} component={Layout}>
      <IndexRoute component={Home} />
      <Route path="home" name="home" component={Home} onEnter={requireAuth} />
      <Route path="login" name="login" component={Login} />
      <Route path="games" name="games" component={Games}></Route>
      <Route path="players" name="players" component={Players}/>
      <Route path="players/:player" component={Players}/>
      <Route path="stats" name="stats" component={Stats}></Route>
      <Route path="teams" name="teams" component={Teams}></Route>
      <Route path="top-stories" name="topStories" component={TopStories}></Route>
    </Route>
  </Router>,
  app
);
