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


load_dotenv()
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_id = os.getenv("HUGGINGFACE_CLIENT_ID")
client_secret = os.getenv("HUGGINGFACE_CLIENT_SECRET")
authorization_base_url = os.getenv("authorization_base_url")
token_url = os.getenv("token_url")
redirect_uri = "http://127.0.0.1:5000/auth/huggingface"


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
            token = "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"
            localdirRepo = "D:\Git\Python\AdminLLMsRepo-1\src\init\repo"  # os.path() is not used correctly here
            repoUrl = create_repo(repo_id=model["modelId"], token=token, exist_ok=True)
            if model["modelId"]:  # Ensure the modelId exists in the model dictionary
                repo = Repository(
                    local_dir=localdirRepo,
                    clone_from=f"https://huggingface.co/{repoUrl}",
                )
                if repo is None:
                    return {"error": "Repo not cloned"}
                return repo
            else:
                return {"error": "Model ID not found in the model dictionary"}
        except Exception as e:
            return {"error": str(e)}
