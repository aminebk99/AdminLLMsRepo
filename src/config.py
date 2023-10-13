import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    