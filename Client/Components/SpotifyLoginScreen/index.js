import React, { Component } from 'react';
import {
  Image,
  StyleSheet,
  Linking,
  Text,
  TouchableHighlight,
  View
} from 'react-native';

import shittyQs from 'shitty-qs';
import CodeInputScreen from '../CodeInputScreen';

const config = require('../../config.js');

export default class SpotifyLoginScreen extends Component {
  constructor(props) {
    super(props);

    this.spotifyOauth = this.spotifyOauth.bind();
  };

  spotifyOauth (client_id, callback) {
    let state = Math.random() + '';
    Linking.addEventListener('url', handleUrl);

    function handleUrl (event) {
      var [, query_string] = event.url.match(/\#(.*)/);
      var query = shittyQs(query_string);
      if (state === query.state) {
        callback(null, query.access_token, query.uid)
      } else {
        callback(new Error('Security Error Encountered.'));
      }
      Linking.removeEventListener('url', handleUrl);
    }

    Linking.openURL(
      'https://accounts.spotify.com/authorize' +
      '?response_type=token' +
      `&client_id=${client_id}` +
      '&scope=user-top-read' +
      '&redirect_uri=group-jam-client://callback' +
      `&state=${state}`
    );
  }

  render() {
    return (
      <View style={styles.mainContainer}>
        <Text style={styles.introText}>
          To Get Started:
        </Text>
        <TouchableHighlight
          style={styles.button}
          onPress={() => this.spotifyOauth(config.client_id, (err, access_token) => {
            if (err) { console.log(err) }
            this.props.navigator.replace({
              component: CodeInputScreen,
              title: 'Success',
              passProps: {
                access_token: access_token,
                navigator: this.props.navigator,
              }
            });
          })}
        >
          <Image
            style={styles.image}
            source={require('../../images/login-button-mobile.png')}
          />
        </TouchableHighlight>
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
  button: {
    justifyContent: 'center',
    alignItems: 'center',
    width: 250,
    height: 50,
    borderRadius: 50,
  },
  image: {
    width: 250,
    height: 50,
    resizeMode: 'contain',
  },
  introText: {
    fontSize: 30,
    textAlign: 'center',
    marginBottom: 15,
    color: 'white',
    fontWeight: 'bold',
  },
});