import os
from flask import Flask , request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .models import *
from .database import db
from .routes import *




app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv('SECRET_KEY')


migrate = Migrate(app, db)

db.init_app(app)


app.register_blueprint(cloudllm_route)
app.register_blueprint(template_blueprint)



@app.route("/")
def hello():
    return "Hello, World!"

