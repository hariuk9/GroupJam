# GroupJam
Intelligent playlists based on a group’s music tastes, using Spotify integration

README

You need to run the web application through Flask by first typing `$ export FLASK_APP=application.py` then `$ flask run`. The web app could be a stand-alone app that generates an optimal playlist for a single user. The first time you log in with your username, you must copy the redirect web address into the terminal prompt and press enter. This will take you to a Spotify login page where you can log in with facebook, email, or any other way you'd usually log into Spotify. The other times, however, your login will be cached so this won't be necessary. However, additional guests must sign in from the mobile app. You can run the mobile app (contained in the Client folder and assuming you have Xcode and iOS simulators installed) by navigating to the Client folder, running `$ npm install` and then `$ react-native run-ios`.

First, navigate to the main page of the web app  and enter your Spotify username. If you don't happen to know your own Spotify username, go to the Spotify desktop app, click on your name in the top right corner, click on the circle with 3 dots under your photo, and select "Copy Spotify URI." The numerals after the last colon are a version of your Spotify username and can be used for login. Upon login, you should see an embedded playlist, intelligently designed just for yourself.

Launch the mobile application as per the instructions above. You'd need another Spotify account to test the group playlist functionality out. Log into the application where promped with your Spotify username and password. After that, your top songs will have been uploaded to our web app.

If you navigate back to the web application and refresh the page, you'll see the playlist has changed! The new songs are picked from both (or more than 2, if you're able to find 3 accounts) Spotify accounts to optimally agree with all users' music tastes. 

