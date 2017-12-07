import React, { Component } from 'react';
import {
  Alert,
  StyleSheet,
  Text,
  View
} from 'react-native';
import IntroScreen from "../IntroScreen/index";

const baseURL = require('../../config.js').base_url;

// In future, should be able to input code to connect to different sessions
export default class CodeInputScreen extends Component {
  constructor(props) {
    super(props);
  };

  componentWillMount() {
    this.sendAccessToken();
  }

  async sendAccessToken() {
    try {
      let response = await fetch(`${baseURL}/auth`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          access_token: `${this.props.access_token}`
        })
      });
      let responseJson = await response.json();
      console.log(responseJson);
    } catch(error) {
      Alert.alert(
        'Error',
        'Unable to connect to host. Please check your connection and try again.',
        [{text: 'OK', onPress: () => this.props.navigator.replace(
            {
              component: IntroScreen,
              title: 'Log In',
            }
            )
          }],
        { cancelable: false }

        )
    }
  }

  render() {
    return (
      <View style={styles.mainContainer}>
        <Text style={styles.introText}>
          Thank you for using GroupJam. Enjoy the playlist personalized for your group!
        </Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  introText: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 15,
    color: 'black',
    fontWeight: 'bold',
  },
});