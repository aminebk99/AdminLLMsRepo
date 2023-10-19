from flask import jsonify, request, session
from requests_oauthlib import OAuth2Session
import os
from dotenv import load_dotenv

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
        print(client_id, client_secret, authorization_base_url, token_url, redirect_uri)
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
        # session["user_id"] = user_info["user_id"]
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
                # You can include other relevant data here
            }
            return response_data
        except Exception as e:
            return {"error": str(e)}  # Return the error message if there's an error
