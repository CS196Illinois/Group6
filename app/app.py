from flask import Flask
from flask import render_template
from flask import request
import datasets
import transformers
# Python standard libraries
import json
import os
import sqlite3

# Third-party libraries
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User

from summarization import Summarizer

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)  

#Login redirect
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

#Login Callback
@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code = code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture, transcripts="", summaries=""
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture, "No transcript", "No summary")
    # Begin user session by logging the user in
    login_user(user)
    # Send user to userpage
    return redirect(url_for("indexSummary"))

#Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("indexSummary"))

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

summarizer = Summarizer('t5-small')

def summarize(s, length_percentage): # make this an actual summarize function
    len_of_data = len(s.split(" "))
    output = summarizer.summarize(s, int(len_of_data*length_percentage/100))

    return output

@app.route('/summarize', methods = ["GET", "POST"])
def indexSummary():
    if request.method == 'GET':
        #Login Functionality
        if current_user.is_authenticated:
            return render_template(r'userpage.html', data="", prefill="", login="You're logged in! Welcome Back, " + current_user.name, profilepic=current_user.profile_pic)
        else:
            return render_template(r'index.html', data="", prefill="", login='')
    else:
        print(request, " - - Post Request detected")
        data = request.form['transcript']
        length= int(request.form['length'])
        print(length)
        return render_template(r'index.html', data=summarize(str(data), length), prefill=data)
        # return text from the webpage

@app.route('/', methods = ["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template(r'landing.html')
    else:
        print(request, " - - Post Request detected")
        data = request.form['transcript']
        length= int(request.form['length'])
        print(length)
        return render_template(r'index.html', data=summarize(str(data), length), prefill=data)
        # return text from the webpage

@app.route('/login/dashboard/')
def loadDashboard():
    return render_template(r'dashboard.html',username="" , lectures="", summaries="", profilepic=current_user.profile_pic)


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
