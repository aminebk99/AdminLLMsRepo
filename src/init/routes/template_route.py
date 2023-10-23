# init/routes/template_route.py
from flask import Blueprint, url_for, current_app, request, jsonify
from authlib.integrations.flask_client import OAuth
from init import controllers
from ..config import Config
import os
import requests
import subprocess


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
def clone_repository():
    data = request.json
    username = data.get("username")
    repo_name = data.get('repo_name')
    destination = data.get('destination', '.')  # Default to current directory if not specified
    token = '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'
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    try:
        response = requests.get(f'https://api.github.com/repos/{username}/{repo_name}', headers=headers)
        if response.status_code == 200:
            destination = os.path.normpath(destination)
            if os.path.exists(destination) and os.path.isdir(destination):
                clone_cmd = ['git', 'clone', f"https://{token}@github.com/{username}/{repo_name}.git", destination]
                cmd = subprocess.run(clone_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                if cmd.returncode == 0:
                    existing_dockerfile_path = 'init/Dockerfile'
                    with open(existing_dockerfile_path, 'r') as existing_dockerfile:
                        dockerfile_content = existing_dockerfile.read()
                    cloned_repo_directory = os.path.join(destination, repo_name)
                    cloned_repo_path = os.path.join(cloned_repo_directory, 'Dockerfile')
                    with open(cloned_repo_path, 'w') as dockerfile:
                        dockerfile.write(dockerfile_content)

                    clone_cmd = ['git', 'add', 'Dockerfile']
                    cmd = subprocess.run(clone_cmd, cwd=cloned_repo_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if cmd.returncode == 0:
                        return jsonify({"message": f"Repository {repo_name} cloned successfully, and Dockerfile added to {cloned_repo_directory}."})
                    else:
                        return jsonify({"error": f"Failed to add Dockerfile to the repository.", "output": cmd.stderr}), 500 
                else:
                    return jsonify({"error": f"Failed to clone repository {repo_name}.", "output": cmd.stderr}), 500
            else:
                return jsonify({"error": "Invalid destination directory."}), 400
        else:
            return jsonify({"error": f"Repository {repo_name} not found or an error occurred."}), 404
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to execute 'git clone': {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500