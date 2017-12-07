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
    this.getTracks().then((ids) => this.sendTracks(ids));
  }

  async getTracks() {
    const limit = 10;
    try {
      let response = await fetch(`https://api.spotify.com/v1/me/top/tracks?limit=${limit}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Authorization': `Bearer ${this.props.access_token}`
        },
      });

      let responseJson = await response.json();
      return responseJson.items.map((track) => track.id);
    } catch(error) {
      Alert.alert(
        'Error',
        'Unable to retrieve data from Spotify. Please check your connection and try again.',
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

  async sendTracks(ids) {
    try {
      let backendResponse = await fetch(`${baseURL}/tracks?track_ids=${ids}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log(backendResponse);
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