from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from .models import *
from .database import db
from .routes import *

from init.routes.template_route import template_route
app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(template_route, url_prefix='/api/v1')

app.secret_key = app.config['SECRET_KEY']

migrate = Migrate(app, db)

db.init_app(app)


app.register_blueprint(example_route)



@app.route("/")
def hello():
    return "Hello, World!"
