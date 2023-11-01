# init/routes/template_route.py
from flask import Blueprint, url_for, current_app, request, jsonify
from authlib.integrations.flask_client import OAuth
from init import controllers
from ..config import Config
import requests


template_route = Blueprint('template', __name__)


oauth = OAuth(current_app)

github = oauth.register(
    name='github',
    client_id=Config.GITHUB_CLIENT_ID,
    client_secret=Config.GITHUB_CLIENT_SECRET,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    client_kwargs={'scope': 'user:email repo'},
)
# Route for initiating the GitHub login
@template_route.route('/login')
def login():
    github_client = oauth.create_client('github')
    redirect_uri = url_for('template.authorize', _external=True)
    print(f"Redirect URI: {redirect_uri}")
    return github_client.authorize_redirect(redirect_uri)

@template_route.route('/authorize')
def authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()

    # Fetch user information
    user_resp = github.get('https://api.github.com/user')
    user_info = user_resp.json()
    email = user_info.get('email', None)
    # github_id = user_info.get('id')

    # Fetch the user's repositories
    repo_resp = github.get('https://api.github.com/user/repos')
    repo_info = repo_resp.json()

    if repo_info:
        # Save the first repository's name and URL
        repo_name = repo_info[0]['name']
        repo_url = repo_info[0]['clone_url']
    else:
        repo_name = "Repository not found in the database"
        repo_url = "Repository URL not found"

    # Check if the user already exists in the database
    # user = User.query.filter_by(github_id=github_id).first()

    # if not user:
    #     # Create a new user record in the database
    #     user = User(github_id=github_id, access_token=token['access_token'], repo_name=repo_name, repo_url=repo_url)
    #     if email:
    #         user.email = email
    #     db.session.add(user)
    #     db.session.commit()
    # else:
    #     # Update the user's access token, repo name, and repo URL in the database
    #     user.access_token = token['access_token']
    #     user.repo_name = repo_name
    #     user.repo_url = repo_url
    #     if email:
    #         user.email = email
    #     db.session.commit()

    return f'Access Token: {token["access_token"]}<br>Hello, {email}<br>!<br>Your repo name is: {repo_name}<br>Repository URL for cloning: {repo_url}'

@template_route.route('/github/repos')
def fetch_all_repos():
    token = request.args.get('token')  
    if not token:
        return jsonify({'error': 'Token not provided'}), 400
    github_api_url = 'https://api.github.com/user/repos'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    response = requests.get(github_api_url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        return jsonify(repos)
    else:
        return jsonify({'error': f'Failed to fetch repositories. Status code: {response.status_code}'}), response.status_code
    
@template_route.route('/github/clone', methods=['POST'])
def clone_private_repo():
    data = request.get_json()
    result = controllers.TemplateController.clone_repos(data)
    return result