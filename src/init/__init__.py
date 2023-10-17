from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from init.routes.template_route import template_route
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(template_route, url_prefix='/api/v1')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route("/")
def hello():
    return "Hello, World!"
