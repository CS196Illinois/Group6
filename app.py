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

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

summarizer = transformers.pipeline("summarization", model = "t5-small")

def summarize(s, length_percentage): # make this an actual summarize function
    len_of_data = len(s.split(" "))
    output = summarizer(s, min_length = 1, max_length = int(len_of_data*length_percentage/100))
    return output[0]['summary_text']

@app.route('/', methods = ["GET", "POST"]) #
def index():
    if request.method == 'GET':
        return render_template(r'index.html', data="", prefill="")
    else:
        print(request, " - - Get Request detected")
        data = request.form['transcript']
        length= int(request.form['length'])
        print(length)
        return render_template(r'index.html', data=summarize(str(data), length), prefill=data)
        # return text from the webpage




app.run()