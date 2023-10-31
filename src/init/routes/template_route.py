# # init/routes/template_route.py
from flask import Blueprint, jsonify, request
from init.controllers.template_controller import TemplateController

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
        return jsonify({"error": str(e)}), 500

# @template_blueprint.route("/api/v1/SelectModelRepo", methods=["get"])
# def select_model_repo():
#     repo = request.args.get("modelId", default=None, type=str)
#     if repo is None:
#         return jsonify({"error": "No repo provided"}), 400
#     else:
#         return controller.selectModelRepo(repo)


# @template_blueprint.route("/api/v1/CloneModelRepo", methods=["get"])
# def clone_model_repo():
#     repo = request.args.get("modelId", default=None, type=str)
#     if repo is None:
#         return jsonify({"error": "No repo provided"}), 400
#     else:
#         try:
#             return controller.cloneModelRepo(repo)
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500


# @template_blueprint.route("/api/v1/createDockerImage", methods=["post"])
# def createDocker():
#     repo = request.json
#     repo_name = repo.get("repo_name", None)
#     repo_path = repo.get("repo_path", None)
#     if repo_name is None:
#         return jsonify({"error": "No repo_name provided"}), 400
#     elif repo_path is None:
#         return jsonify({"error": "No repo_path provided"}), 400
#     else:
#         try:
#             return controller.createDockerImage(repo_path, repo_name)
#         except Exception as e:
#             return jsonify({"error route": str(e)}), 500
