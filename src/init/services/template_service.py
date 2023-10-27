from init import db
from init.models import LLMType, LLMTemplate
from flask import session, url_for, jsonify, redirect  
from ..config import Config
import subprocess
import os
import docker
from docker.errors import BuildError, APIError, DockerException, ImageNotFound


class TemplateService:
    def loginWithGithub(github):
        callback_url = url_for('authorized', _external=True)
        return github.authorize_redirect(callback=callback_url)


    def clone_repository(username, repo_name, token_user):
        try:
            current_directory = os.getcwd()
            file_name = 'Dockerfile'
            repos_folder = os.path.join(current_directory, 'deployment', repo_name)
            clone_url = f"https://{token_user}@github.com/{username}/{repo_name}.git"
            file_path = os.path.join(repos_folder, file_name)

            subprocess.run(["git", "clone", clone_url, repos_folder], check=True)

            with open('./docker/dockerfile', 'r') as firstfile, open(file_path, 'a') as secondfile:
                for line in firstfile:
                    secondfile.write(line)

            return repos_folder
        except subprocess.CalledProcessError as e:
            print(f"Subprocess error: {e}")
            None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def build_docker_image(repo_path, repo_name, tag='latest'):
        try:
            repo_name = repo_name.lower()
            client = docker.from_env()
            print(f"Building image from {repo_path}")
            image, build_log = client.images.build(path=repo_path, tag=f"{repo_name}:{tag}")

            for line in build_log:
                print(line)

            print(f"Image built: {image}")
            image
        except BuildError as build_err:
            print(f"Build error: {build_err}")
            return None
        except APIError as api_err:
            print(f"API error: {api_err}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def push_docker_image(image, acr_login_server, acr_username, acr_password, tag='latest'):
        try:
            client = docker.from_env()
            client.login(username=acr_username, password=acr_password, registry=acr_login_server)
            full_image_name = image.tags[0]
            image_name = full_image_name.split('/')[-1].split(':')[0]
            print(f"Tagging image {image_name} with tag {tag}")
            image.tag(f"{acr_login_server}/{image_name}", tag=tag)
            client.images.push(f"{acr_login_server}/{image_name}", tag=tag)

            session['image_info'] = {
                'name': image_name,
                'tag': tag,
                'registry': acr_login_server
            }
            return session['image_info']
        except DockerException as login_err:
            print(f"Login error: {login_err}")
            return None
        except ImageNotFound as tag_err:
            print(f"Tagging error: {tag_err}")
            return None
        except IndexError as index_err:
            print(f"Index error: {index_err}")
            return None
        except APIError as push_err:
            print(f"Push error: {push_err}")
            return None
