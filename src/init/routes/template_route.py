# init/routes/template_route.py
from flask import Blueprint, request, current_app
from init.controllers.template_controller import TemplateController
from authlib.integrations.flask_client import OAuth
from ..config import Config

template_route = Blueprint('template', __name__)
controller = TemplateController()
oauth = OAuth()

github = oauth.register(
    name='github',
    client_id='your_github_client_id',
    client_secret='your_github_client_secret',
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    authorize_params_callback=None,
    authorize_extra_params=None,
    authorize_url_params=None,
    authorize_response_callback=None,
    client_kwargs={'scope': 'user:email'},
    request_token_url=None,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000//login/callback/github',
    client_cls=None,
    client=none,
)

@template_route.route('/login/github', methods=['GET'])
def login_with_github():
    return controller.login_with_github(github)

@template_route.route('/login/callback/github', methods=['GET'])
def call_back_login_with_github():
    return controller.callback_github(github)

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
