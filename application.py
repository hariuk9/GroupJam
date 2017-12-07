from cs50 import SQL
import sys
import spotipy
import spotipy.util as util
from flask import Flask, flash, redirect, render_template, request, session
#from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Configure application
app = Flask(__name__)

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

#db = SQL("sqlite:///finance.db")

#initializing the authentication token to something
auth = 0

#@app.route("/auth", methods = ["GET", "POST"])
#def auth_user():

aggregate = {"danceability": 0.0,
    "energy": 0.0,
    "key": 0.0,
    "loudness": 0.0,
    "mode": 0.0,
    "speechiness": 0.0,
    "acousticness": 0.0,
    "instrumentalness": 0.0,
    "liveness": 0.0,
    "valence": 0.0,
    "tempo": 0.0
}

@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/authorize", methods=["GET", "POST"])
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

def score(songs):
    for




    url = "idk" #the get request for the
    r = requests.get(url)
    data=r.json()


