import React, {Component} from 'react';
import {
  StyleSheet,
  Text,
  View,
  Image,
  TouchableOpacity,
} from 'react-native';

import Swiper from 'react-native-swiper';

import SpotifyLoginScreen from "../SpotifyLoginScreen/index";

export default class IntroScreen extends Component {
  render() {
    return (
      <Swiper style={styles.wrapper} showsButtons={false} autoplay={true} autoplayTimeout={3.5}>
        <View style={styles.slide1}>
          <Text style={styles.text}>Welcome to GroupJam!</Text>
          <Text style={styles.infoText}>Powered by</Text>
          <Image style={styles.logo} source={require('../../images/SpotifyLogo.png')}/>
        </View>
        <View style={styles.slide2}>
          <Text style={styles.text}>Intelligent, dynamic playlists based on a group’s music tastes.</Text>
        </View>
        <View style={styles.slide3}>
          <SpotifyLoginScreen navigator={this.props.navigator}/>
        </View>
      </Swiper>
    );
  }
}


const styles = StyleSheet.create({
  wrapper: {
  },
  slide1: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#9DD6EB',
  },
  slide2: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#97CAE5',
  },
  slide3: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#92BBD9',
  },
  text: {
    marginVertical: 15,
    color: '#ffffff',
    fontSize: 30,
    fontWeight: 'bold',
  },
  infoText: {
    color: '#ffffff',
    fontSize: 20,
  },
  logo: {
    height: 100,
    width: 200,
    resizeMode: 'contain',
  },
  buttonText: {
    marginTop: 20,
    fontSize: 24,
    fontWeight: 'bold',
    color: 'green',
  }
});