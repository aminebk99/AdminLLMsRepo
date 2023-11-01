from flask import redirect, request, jsonify
from init.services.template_service import TemplateService
import json
# init/controllers/template_controller.py
from flask import request, jsonify
from init.services import TemplateService
import requests

class TemplateController:

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
