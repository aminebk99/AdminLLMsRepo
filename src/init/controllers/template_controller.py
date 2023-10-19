# # init/controllers/template_controller.py
from flask import redirect, request, jsonify
from init.services.template_service import TemplateService

class TemplateController:
    def __init__(self):
        self.template_service = TemplateService()

#     def login_with_github(self):
#         try:
#             token = self.template_service.loginWithGithub()
#             return jsonify({"access_token": token}), 200
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

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



#     def fetch_models_from_huggingface(self):
#         try:
#             models = self.template_service.fetchModelsFromHuggingFace()
#             return jsonify(models), 200
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     def create_docker_image(self, model_id):
#         try:
#             self.template_service.createDockerImage(model_id)
#             return jsonify({"message": "Docker image creation in progress"}), 202
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     def fetch_github_repos(self):
#         try:
#             user_token = request.headers.get("Authorization")
#             repos = self.template_service.fetchGithubRepos(user_token)
#             return jsonify(repos), 200
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     def create_cloud_llm_template(self):
#         try:
#             template_data = request.get_json()
#             self.template_service.createCloudLLMTemplate(template_data)
#             return jsonify({"message": "Cloud LLM template created"}), 201
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     def get_template(self, template_id):
#         try:
#             template = self.template_service.getTemplate(template_id)
#             if template:
#                 return jsonify(template), 200
#             else:
#                 return jsonify({"message": "Template not found"}), 404
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500
