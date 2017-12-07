import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from flask import abort, Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp

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

# list of track ids gathered from users
tracks = []

@app.route("/tracks", methods = ["POST"])
def get_user_tracks():
    # retrieve top tracks from newly connected user
    ids = json.loads(request.data)['ids']
    tracks.extend(ids)

    return 'success'

@app.route("/")
@login_required
def index():
    username = session["username"]
    # host has already logged in and playlist is already made
    if session.get("token") and session.get("playlist_dict"):
        group_playlist = gen_playlist(tracks)
        sp = spotipy.Spotify(auth=session["token"])
        playlist = sp.user_playlist_add_tracks(username, session["playlist_dict"]['id'], group_playlist) # add to the playlist
        return render_template("index.html", playlist_url=session["playlist_dict"]['uri'])

    # perfom oauth and create group playlist
    token = util.prompt_for_user_token(username,'playlist-modify-public user-top-read');
    if token:
        session["token"] = token
        sp = spotipy.Spotify(auth=token)
        track_dict = sp.current_user_top_tracks(limit=20, offset=0, time_range='medium_term') # get the hosts top tracks
        tracks = list(map(lambda x: x['id'], track_dict['items']))
        group_playlist = gen_playlist(tracks)

        playlist_dict = sp.user_playlist_create(username, "Group Playlist")
        playlist_id = playlist_dict['id']
        user = playlist_dict['owner']

        playlist = sp.user_playlist_add_tracks(username, playlist_id, group_playlist) # playlist is now populated
    else:
        print("Can't get token for " + username)

    url = "https://open.spotify.com/embed?uri=" + playlist_dict['uri']
    session["playlist_url"] = playlist_dict['uri']
    return render_template("index.html", playlist_url=url)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    tracks = []

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if request.form.get("username"):
            session["username"] = request.form.get("username")
            return redirect("/")

    else:
        return render_template("login.html")


def compare_score(song, total_features, features):
    score=0.0
    for key, value in features[0].items():
        if isinstance(value, float):
            score+=(value*1.0)/((1.0)*(total_features[key]+value))
    return score

def gen_playlist(track_ids):
    """Determine which tracks (capped at 20) best suit the group"""
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    total_features={"danceability":0.0, "energy":0.0, "key":0.0, "loudness":0.0, "mode":0.0, "speechiness":0.0, "acousticness":0.0, "instrumentalness":0.0, "liveness":0.0, "valence":0.0, "tempo":0.0}
    song_counter=0.0
    
    for song in track_ids:
        song_counter += 1
        features = sp.audio_features(tracks=[song])
        for key, value in features[0].items():
            if isinstance(value, float):
                total_features[key] += value
        
    if song_counter > 0:
        for key, value in total_features.items():
            value /= song_counter

    # now we find all the songs close enough to the "average"
    song_list=[]
    for song in track_ids:
        score = compare_score(song, total_features, sp.audio_features(tracks=[song]))
        song_list.append((song, score))
    song_list = sorted(song_list, key = lambda x: x[1])

    if len(song_list) > 20:
        song_list = song_list[:20]
    song_list = [song_list[i][0] for i in range(len(song_list))]
    return song_list




