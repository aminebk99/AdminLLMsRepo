from init import db
from init.models import LLMTemplate
from flask import session, url_for, jsonify, redirect  
from ..config import Config
import docker
from docker.errors import BuildError, APIError, DockerException, ImageNotFound
from flask import jsonify, request, session
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv
from huggingface_hub import (
    HfApi,
    list_models,
    login,
    hf_hub_download,
    Repository,
    create_repo,
)
import docker
from docker.errors import BuildError, APIError

load_dotenv()
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_id = os.getenv("HUGGINGFACE_CLIENT_ID")
client_secret = os.getenv("HUGGINGFACE_CLIENT_SECRET")
authorization_base_url = os.getenv("authorization_base_url")
token_url = os.getenv("token_url")
redirect_uri = "http://127.0.0.1:5000/auth/huggingface"
huggingfaceToken = os.getenv("huggingfaceToken")


class TemplateService:
    @staticmethod
    def get_oauth_session(state=None):
        if client_id is None:
            raise ValueError("Missing environment variable: HUGGINGFACE_CLIENT_ID")
        return OAuth2Session(client_id, state=state, redirect_uri=redirect_uri)

    @staticmethod
    def Callback():
        oauth_state = session.get("oauth_state")
        if oauth_state is None:
            return jsonify({"error": "OAuth state not found"}), 400
        huggingface = OAuth2Session(
            client_id, state=oauth_state, redirect_uri=redirect_uri, token={}
        )

        token = huggingface.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=request.url,
        )
        session["oauth_token"] = token
        user_info = huggingface.get("https://huggingface.co/oauth/userinfo").json()
        # tokens = huggingface.get("https://huggingface.co/oauth/authorize").json()
        return jsonify(user_info), 200

    @staticmethod
    def loginWithHuggingFace():
        try:
            huggingface = TemplateService.get_oauth_session()
            authorization_url, state = huggingface.authorization_url(
                authorization_base_url
            )
            session["oauth_state"] = state
            response_data = {
                "authorization_url": authorization_url,
                "token_url": token_url,
            }
            return response_data
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def fetchModelsFromHuggingFace(query, page):
        api = HfApi()
        models = api.list_models(search=query, cardData=True)

        model_list = [
            {
                "modelId": model.modelId,
                "sha": model.sha,
                "lastModified": model.lastModified,
                "tags": model.tags,
                "pipeline_tag": model.pipeline_tag,
                "siblings": [str(sibling) for sibling in model.siblings],
                "id": model.id,
                "private": model.private,
                "likes": model.likes,
                "downloads": model.downloads,
            }
            for model in models
        ]

        searchLen = len(model_list)
        pageZero = 10 * (page - 1)
        pageLast = 10 * page

        listModels = {
            "pages": searchLen // 10 + 1,
            "currentPage": page,
            "total": len(model_list),
            "models": model_list[pageZero:pageLast],
        }

        return listModels

    @staticmethod
    def selectModelRepo(modelId):
        api = HfApi()
        model = api.model_info(modelId)
        modelInfo = {
            "modelId": model.modelId,
            "sha": model.sha,
            "lastModified": model.lastModified,
            "tags": model.tags,
            "pipeline_tag": model.pipeline_tag,
            "siblings": [str(sibling) for sibling in model.siblings],
            "id": model.id,
            "private": model.private,
            "likes": model.likes,
            "downloads": model.downloads,
        }
        return modelInfo

    @staticmethod
    def cloneModelRepo(modelId):
        try:
            model = TemplateService.selectModelRepo(modelId)
            token = huggingfaceToken
            targetdir = os.path.join(os.getcwd(), "models", model["modelId"])
            repoUrl = create_repo(repo_id=model["modelId"], token=token, exist_ok=True)
            if model["modelId"]:
                repo = Repository(
                    local_dir=targetdir,
                    clone_from=f"https://huggingface.co/{repoUrl}",
                )
                if repo is None:
                    return {"error": "Repo not cloned"}
                
                data = {
                    "path":repo.local_dir,
                    "repo_name":model["modelId"],
                }
                return data
            else:
                return {"error": "Model ID not found in the model dictionary"}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def ensure_dockerfile_exists(path):
        dockerfile_path = os.path.join(path, "Dockerfile")
        if not os.path.isdir(path):
            return f"Directory does not exist: {path}"
        elif not os.path.isfile(dockerfile_path):
            try:
                with open(dockerfile_path, "w") as f:
                    f.write(
                        "FROM python:3.8-slim-buster\n"
                    )  # This is a basic Dockerfile for a Python app
                return f"Dockerfile created at {dockerfile_path}"
            except Exception as e:
                return f"Failed to create Dockerfile: {e}"
        else:
            return f"Dockerfile already exists at {dockerfile_path}"

    @staticmethod
    def createDockerImage(repo_path, repo_name, tag="latest"):
        check = TemplateService.ensure_dockerfile_exists(repo_path)
        if "error" in check:
            return check
        client = docker.from_env()
        try:
            repo_name = repo_name.lower()
            image, build_log = client.images.build(
                path=repo_path, tag=f"{repo_name}:{tag}"
            )
            for line in build_log:
                print(line)
            image_info: dict = {
                "id": image.id,
                "tags": image.tags,
                "short_id": image.short_id,
                "attrs": image.attrs,
            }
            return image_info
        except (BuildError, APIError) as err:
            return f"error: {str(err)}"
        except Exception as e:
            return f"unexpected error: {str(e)}"
    
    @staticmethod
    def loginWithGithub(github):
        callback_url = url_for('/authorized', _external=True)
        return github.authorize_redirect(callback=callback_url)
<<<<<<< HEAD
    
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

=======

    @staticmethod
    def clone_repository(username, repo_name, token_user):
        try:
            current_directory = os.getcwd()
            file_name = 'Dockerfile'
            repos_folder = os.path.join(current_directory, 'deployment', repo_name)
            print(f"token_user: {token_user}")
            print(f"username: {username}")
            print(f"repo_name: {repo_name}")
            clone_url = f"https://{token_user}@github.com/{username}/{repo_name}.git"
            file_path = os.path.join(repos_folder, file_name)

            subprocess.run(["git", "clone", clone_url, repos_folder], check=True)

            with open('./docker/dockerfile', 'r') as firstfile, open(file_path, 'a') as secondfile:
                for line in firstfile:
                    secondfile.write(line)

            return repos_folder
        except subprocess.CalledProcessError as e:
            print(f"Subprocess error: {e}")
            return None  
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
    
    @staticmethod
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

    
>>>>>>> aff87731dd153a6d7462312acd6d2825a01d880a
