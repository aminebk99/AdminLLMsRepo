# init/routes/template_route.py
from flask import Blueprint, redirect
from authlib.integrations.flask_client import OAuth
from init import controllers
from ..config import Config
import os

# Define the blueprint for the template routes
template_route = Blueprint('template', __name__)

# Initialize OAuth
oauth = OAuth()

def configure_github_oauth():
    github = oauth.register(
        name='github',
        client_id=Config.GITHUB_CLIENT_ID,
        client_secret=Config.GITHUB_CLIENT_SECRET,
        authorize_url='https://github.com/login/oauth/authorize',
        client_kwargs={'scope': 'user:email'},
        redirect_uri='http://localhost:5000/login/callback/github'  
    )
    return github


@template_route.route('/login/github', methods=['GET'])
def login_with_github():
    github = configure_github_oauth()
    return redirect(github.authorize_redirect())


@template_route.route('/login/callback/github', methods=['GET'])
def call_back_login_with_github():
    github = configure_github_oauth()
    token = github.authorize_access_token()
    user = github.parse_id_token(token)
    # Handle user data as needed
    return f'Hello, {user["sub"]}'

