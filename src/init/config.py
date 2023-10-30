import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+mysqlconnector://root:secret@src_db/llmsdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'F974135B4E19A99341FDA8963BE52'

    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID') or 'df808e46cf929ecccaac'
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET') or '2422d2df4e658ae2aee64c712269036215c3c0d9'

    ACR_LOGIN_SERVER = os.environ.get('ACR_LOGIN_SERVER') or 'bafcloudregistry.azurecr.io'
    ACR_USERNAME = os.environ.get('ACR_USERNAME') or 'bafcloudregistry'
    ACR_PASSWORD = os.environ.get('ACR_PASSWORD') or 'X1I+OiBzcpOYKs4Y4jNKWPGfAhjy9Z6/94hfvZKNGP+ACRDlU+eB'
