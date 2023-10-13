import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app = Flask(__name__)
