import React, { Component } from 'react';
import {
  NavigatorIOS,
} from 'react-native';

import IntroScreen from "../IntroScreen/index";

export default class MainNavigator extends Component {
  render() {
    return (
      <NavigatorIOS
        initialRoute={{
          component: IntroScreen,
          title: 'Log In',
        }}
        style={{flex: 1}}
        navigationBarHidden={true}
      />
    );
  }
}
