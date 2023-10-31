from flask import redirect, request, jsonify
from init.services.template_service import TemplateService
import json
class TemplateController:
    def __init__(self):
        self.template_service = TemplateService()

    def login_with_huggingface(self):
        try:
            response = self.template_service.loginWithHuggingFace()
            if 'error' in response:
                return jsonify(response), 500
            else:
                return redirect(response['authorization_url'])
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        
    def Callback(self):
        try:
            response, status = self.template_service.Callback()
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def fetch_models_from_huggingface(self,query,page ):
        try:
            models = self.template_service.fetchModelsFromHuggingFace(query=query,page=page)
            return jsonify(models), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def selectModelRepo(self, model_id):
        try:
            response = self.template_service.selectModelRepo(model_id)
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def cloneModelRepo(self, model_id):
        try:
            response = self.template_service.cloneModelRepo(model_id)
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    def createDockerImage(self,  repo_path,repo_name ):
        try:
            response = self.template_service.createDockerImage(repo_path,repo_name )
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"error control": str(e)}), 500