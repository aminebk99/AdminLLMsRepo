import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:secret@src_db/llmsdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app = Flask(__name__)
    
    #Github
    GITHUB_CLIENT_ID = 'df808e46cf929ecccaac'
    GITHUB_CLIENT_SECRET = '2422d2df4e658ae2aee64c712269036215c3c0d9'
    

    ACR_LOGIN_SERVER = 'bafcloudregistry.azurecr.io'
    ACR_USERNAME = 'bafcloudregistry'
    ACR_PASSWORD = 'X1I+OiBzcpOYKs4Y4jNKWPGfAhjy9Z6/94hfvZKNGP+ACRDlU+eB'
