# init/controllers/template_controller.py
from flask import request, jsonify
from init.services import TemplateService
import requests

class TemplateController:


    def login_with_github(self, github):  # Add 'self' as the first parameter
        try:
            service = TemplateService.loginWithGithub(github)
            return service
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def callback_github(self, github):  # Add 'self' as the first parameter
        token = github.authorize_access_token()
        if token:
            return token
        else:
            return 'Access denied', 400



    def login_with_huggingface():
        try:
            token = TemplateService.loginWithHuggingFace()
            return jsonify({"access_token": token}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def fetch_models_from_huggingface():
        try:
        # Define the Hugging Face models API endpoint
            huggingface_models_url = "https://api-inference.huggingface.co/models"

        # Send a GET request to the Hugging Face API to fetch the available models
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
            # repos = TemplateService.fetchGithubRepos(user_token)
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
