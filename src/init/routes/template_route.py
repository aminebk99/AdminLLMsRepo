# # init/routes/template_route.py
from flask import Blueprint, jsonify, request
from init.controllers.template_controller import TemplateController

template_blueprint = Blueprint('template', __name__)
controller = TemplateController()

# @template_blueprint.route('/api/v1/login/github', methods=['POST'])
# def login_with_github():
#     return controller.login_with_github()

@template_blueprint.route('/api/v1/login/huggingface', methods=['get'])
def login_with_huggingface():
    return controller.login_with_huggingface()


@template_blueprint.route('/auth/huggingface', methods=['GET'])
def callback():
    return controller.Callback()


# @template_blueprint.route('/api/v1/models', methods=['GET'])
# def fetch_models_from_huggingface():
#     return controller.fetch_models_from_huggingface()

# @template_blueprint.route('/api/v1/docker-image/<int:model_id>', methods=['POST'])
# def create_docker_image(model_id):
#     return controller.create_docker_image(model_id)

# @template_blueprint.route('/api/v1/github/repos', methods=['GET'])
# def fetch_github_repos():
#     return controller.fetch_github_repos()

# @template_blueprint.route('/api/v1/template', methods=['POST'])
# def create_cloud_llm_template():
#     return controller.create_cloud_llm_template()

# @template_blueprint.route('/api/v1/template/<int:template_id>', methods=['GET'])
# def get_template(template_id):
#     return controller.get_template(template_id)
