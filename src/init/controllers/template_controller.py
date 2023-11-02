from flask import redirect, request, jsonify
from init.services.template_service import TemplateService
import json
# init/controllers/template_controller.py
from flask import request, jsonify
from init.services import TemplateService
import requests
from ..config import Config
from init.services import clone_repo, push_repo, save_data_template

class TemplateController:
    def clone_repos(data):
        repo_name = data.get('repo_name')
        username = data.get('username')
        description = data.get('description')
        tags = data.get('tags')
        type = data.get('type')
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
                    save_data_template(name = repo_name, description = description, image_url = result, type = type, tags = tags)
                    return jsonify({"message": f"Image built and pushed to ACR: {repo_name}"})
                else:
                    return jsonify({"error": "Failed to push Docker image to ACR"}), 500
            else:
                return jsonify({"error": "Failed to build Docker image"}), 500
        else:
            return jsonify({"error": "Failed to clone the repository"}), 500

    template = TemplateService()
    def login_with_huggingface(self):
        try:
            token = self.template.loginWithHuggingFace()
            return jsonify({"access_token": token}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def Callback(self):
        try:
            response, status = self.template.Callback()
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def fetch_models_from_huggingface(self,query,page ):
        try:
            models = self.template.fetchModelsFromHuggingFace(query=query,page=page)
            return jsonify(models), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def selectModelRepo(self,model_id):
        try:
            response = self.template.selectModelRepo(model_id)
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def cloneModelRepo(self,model_id):
        try:
            response = self.template.cloneModelRepo(model_id)
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def createDockerImage(self,repo_path,repo_name):
        try:
            response = self.template.createDockerImage(repo_path,repo_name )
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"error control": str(e)}), 500

        
    def fetch_github_repos():
        try:
            user_token = request.headers.get("Authorization")
            return jsonify( user_token), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def create_cloud_llm_template(self):
        try:
            template_data = request.get_json()
            self.template.createCloudLLMTemplate(template_data)
            return jsonify({"message": "Cloud LLM template created"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_template(self,template_id):
        try:
            template = self.template.getTemplate(template_id)
            if template:
                return jsonify(template), 200
            else:
                return jsonify({"message": "Template not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
