# init/routes/template_route.py
from flask import Blueprint, redirect
from authlib.integrations.flask_client import OAuth
from ..config import Config

template_route = Blueprint('template', __name__)
oauth = OAuth()

def configure_github_oauth():
    github = oauth.register(
        name='github',
        client_id=Config.GITHUB_CLIENT_ID,
        client_secret=Config.GITHUB_CLIENT_SECRET,
        authorize_url='https://github.com/login/oauth/authorize',
        client_kwargs={'scope': 'user:email'},
        redirect_uri='http://localhost:5000/login/callback/github'  # Update with your callback URL
    )
    return github

@template_route.route('/login/github_oauth', methods=['GET'])
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

@template_route.route('/login/huggingface', methods=['POST'])
def login_with_huggingface():
    return controller.login_with_huggingface()

@template_route.route('/models', methods=['GET'])
def fetch_models_from_huggingface():
    return controller.fetch_models_from_huggingface()

@template_route.route('/docker-image/<int:model_id>', methods=['POST'])
def create_docker_image(model_id):
    return controller.create_docker_image(model_id)

@template_route.route('/github/repos', methods=['GET'])
def fetch_github_repos():
    return controller.fetch_github_repos()

@template_route.route('/template', methods=['POST'])
def create_cloud_llm_template():
    return controller.create_cloud_llm_template()

@template_route.route('/template/<int:template_id>', methods=['GET'])
def get_template(template_id):
    return controller.get_template(template_id)
