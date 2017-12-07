import json
import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from flask import abort, Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

client_id = '320606726d354474b5da64233babe82d'
client_secret = 'f2d15a0b056343cfa094525adfc45f27'

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

tracks = [u'0DAsxISzun85PbsqAfIzeC', u'5lLuArl5DPSd0pYVl9KOWD', u'4uhvMW7ly7tJil31YYscAN', u'7vGuf3Y35N4wmASOKLUVVU', u'7t2bFihaDvhIrd2gn2CWJO', u'5Z3GHaZ6ec9bsiI5BenrbY', u'47OVNnZJzIkrsEiZ4n187p', u'1OmcAT5Y8eg5bUPv9qJT4R', u'6QgjcU0zLnzq5OrUoSZ3OK', u'7HNpXPaTcX5CoNBjTAEWBr']


@app.route("/tracks", methods = ["POST"])
def get_user_tracks():
    ids = json.loads(request.data)['ids']
    tracks.extend(ids)

    print(tracks)
    return 'success'

@app.route("/")
#@login_required
def index():
    group_playlist = gen_playlist(tracks)
    print(group_playlist)
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


def compare_score(song, total_features):
    score=0.0
    features = sp.audio_features(song)
    for key, value in features:
        score+=(value*1.0)/((1.0)*(total_features.key+value))
    return score

def gen_playlist(track_ids):
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    total_features={}
    song_counter=0.0
    for song in track_ids:
        song_counter+=1
        features = sp.audio_features(tracks=[song])
        for key, value in features:
            total_features.key += value
    for value in total_features.items():
        value /= song_counter

    #now we find all the songs close enough to the "average"
    song_list=[]
    for song in track_ids:
        score = compare_score(song, total_features)
        song_list.append((song, score))
    song_list = sorted(song_list, key = lambda x: x[1])

    if len(song_list) > 20:
        song_list = song_list[:20]

    return song_list




