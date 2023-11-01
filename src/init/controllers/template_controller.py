# init/controllers/template_controller.py
from flask import request, jsonify
from init.services import TemplateService
import requests
from ..config import Config
from init.services import clone_repo, push_repo

class TemplateController:
    def clone_repos(self):
        repo_name = self.get('repo_name')
        username = self.get('username')
        token_user = request.headers['Authorization']
        ACR_LOGIN_SERVER = Config.ACR_LOGIN_SERVER
        ACR_USERNAME = Config.ACR_USERNAME
        ACR_PASSWORD = Config.ACR_PASSWORD
    
        if token_user is None:
            return jsonify({"error": "Authorization header is missing"}), 400
        if token_user.startswith('Bearer '):
            token_user = token_user[7:]  
        else:
            return jsonify({"error": "Invalid Authorization header format"}), 400
        repo_folder = clone_repo.clone_repository(username, repo_name, token_user)
        if repo_folder:
            image = TemplateService.build_docker_image(repo_folder, repo_name)
            if image:
                result = push_repo.push_docker_image(image, ACR_LOGIN_SERVER, ACR_USERNAME, ACR_PASSWORD)
                if result:
                    return jsonify({"message": f"Image built and pushed to ACR: {repo_name}"})
                else:
                    return jsonify({"error": "Failed to push Docker image to ACR"}), 500
            else:
                return jsonify({"error": "Failed to build Docker image"}), 500
        else:
            return jsonify({"error": "Failed to clone the repository"}), 500

    def login_with_huggingface():
        try:
            token = TemplateService.loginWithHuggingFace()
            return jsonify({"access_token": token}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    def fetch_models_from_huggingface():
        try:
            huggingface_models_url = "https://api-inference.huggingface.co/models"
            response = requests.get(huggingface_models_url)
            if response.status_code == 200:
                models_data = response.json()
                model_names = [model['model_id'] for model in models_data]
                return jsonify({'models': model_names})

            else:
                return jsonify({'error': 'Failed to fetch models from Hugging Face'})
        except Exception as e:
            return jsonify({'error': str(e)})

    def create_docker_image( model_id):
        try:
            TemplateService.createDockerImage(model_id)
            return jsonify({"message": "Docker image creation in progress"}), 202
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def fetch_github_repos():
        try:
            user_token = request.headers.get("Authorization")
            return jsonify( user_token), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def create_cloud_llm_template():
        try:
            template_data = request.get_json()
            TemplateService.createCloudLLMTemplate(template_data)
            return jsonify({"message": "Cloud LLM template created"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_template( template_id):
        try:
            template = TemplateService.getTemplate(template_id)
            if template:
                return jsonify(template), 200
            else:
                return jsonify({"message": "Template not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
