import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:secret@localhost/llmsdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

GITHUB_CLIENT_ID = 'df808e46cf929ecccaac'
GITHUB_CLIENT_SECRET = '2422d2df4e658ae2aee64c712269036215c3c0d9'
# HUGGINGFACE_API_KEY = 'your_huggingface_api_key'