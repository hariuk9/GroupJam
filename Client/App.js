import React, { Component } from 'react';
import {
  Linking,
  Platform,
  StyleSheet,
  Text,
  View
} from 'react-native';

import MainNavigator from "./Components/MainNavigator/index";

import shittyQs from 'shitty-qs';
const config = require('./config.js');

export default class App extends Component {

  render() {
    return (
      <MainNavigator/>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
});
