# # init/routes/template_blueprint.py
from flask import Blueprint, jsonify, request
from init.controllers.template_controller import TemplateController
from flask import Blueprint, url_for, current_app, request, jsonify
from authlib.integrations.flask_client import OAuth
from init import controllers
from ..config import Config
import requests

template_blueprint = Blueprint("template", __name__)
controller = TemplateController()


@template_blueprint.route("/api/v1/login/huggingface", methods=["get"])
def login_with_huggingface():
    return controller.login_with_huggingface()


@template_blueprint.route("/auth/huggingface", methods=["GET"])
def callback():
    return controller.Callback()


@template_blueprint.route("/api/v1/SearchModels", methods=["GET"])
def fetch_models_from_huggingface():
    page = request.args.get("page", default=1, type=int)
    query = request.args.get("query", default=None, type=str)
    if query is None:
        # Return something else
        return jsonify({"error": "No query provided"}), 400
    elif page is None:
        return controller.fetch_models_from_huggingface(query, 1)
    else:
        return controller.fetch_models_from_huggingface(query, page)


@template_blueprint.route("/api/v1/CloneFromHugginFace", methods=["get"])
def clone_from_huggingface():
    model_id = request.args.get("modelId", default=None, type=str)
    if model_id is None:
        return jsonify({"error": "No modelId provided"}), 400
    try:
        modelID = controller.selectModelRepo(model_id)
        if "error" in modelID:
            return jsonify(modelID), 500

        clone = controller.cloneModelRepo(model_id)
        if "error" in clone:
            return jsonify(clone), 500
        controller.createDockerImage(clone["path"], clone["repo_name"])
        return jsonify({"success": "Docker Image Created"}), 200
    except Exception as e:
        return jsonify({"error": str(e) }), 500


oauth = OAuth(current_app)

github = oauth.register(
    name="github",
    client_id=Config.GITHUB_CLIENT_ID,
    client_secret=Config.GITHUB_CLIENT_SECRET,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    client_kwargs={"scope": "user:email repo"},
)


# Route for initiating the GitHub login
@template_blueprint.route("/api/v1/login")
def login():
    github_client = oauth.create_client("github")
    redirect_uri = url_for("template.authorize", _external=True)
    print(f"Redirect URI: {redirect_uri}")
    return github_client.authorize_redirect(redirect_uri)


@template_blueprint.route("/api/v1/authorize")
def authorize():
    github = oauth.create_client("github")
    token = github.authorize_access_token()

    # Fetch user information
    user_resp = github.get("https://api.github.com/user")
    user_info = user_resp.json()
    email = user_info.get("email", None)
    # github_id = user_info.get('id')

    # Fetch the user's repositories
    repo_resp = github.get("https://api.github.com/user/repos")
    repo_info = repo_resp.json()

    if repo_info:
        # Save the first repository's name and URL
        repo_name = repo_info[0]["name"]
        repo_url = repo_info[0]["clone_url"]
    else:
        repo_name = "Repository not found in the database"
        repo_url = "Repository URL not found"

    return f'Access Token: {token["access_token"]}<br>Hello, {email}<br>!<br>Your repo name is: {repo_name}<br>Repository URL for cloning: {repo_url}'


@template_blueprint.route("/api/v1/github/repos")
def fetch_all_repos():
    token = request.args.get("token")
    if not token:
        return jsonify({"error": "Token not provided"}), 400
    github_api_url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(github_api_url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        return jsonify(repos)
    else:
        return (
            jsonify(
                {
                    "error": f"Failed to fetch repositories. Status code: {response.status_code}"
                }
            ),
            response.status_code,
        )


@template_blueprint.route("/github/clone", methods=["POST"])
def clone_private_repo():
    data = request.get_json()
    result = controllers.TemplateController.clone_repos(data)
    return result
