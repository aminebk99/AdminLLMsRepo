from init import db
from init.models import LLMType, LLMTemplate
from flask import session, url_for, jsonify, redirect  
from ..config import Config
import docker
from docker.errors import BuildError, APIError, DockerException, ImageNotFound


class TemplateService:
    def loginWithGithub(github):
        callback_url = url_for('authorized', _external=True)
        return github.authorize_redirect(callback=callback_url)
    
    def build_docker_image(repo_path, repo_name, tag='latest'):
        try:
            repo_name = repo_name.lower()
            client = docker.from_env()
            print(f"Building image from {repo_path}")
            image, build_log = client.images.build(path=repo_path, tag=f"{repo_name}:{tag}")

            for line in build_log:
                print(line)

            print(f"Image built: {image}")
            return image  
        except BuildError as build_err:
            print(f"Build error: {build_err}")
            return None
        except APIError as api_err:
            print(f"API error: {api_err}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

