from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from models.User import User , db
from models.Post import Post , db
load_dotenv('.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db.init_app(app)  # Initialize db with the app
migrate = Migrate(app, db)

@app.route('/')
def hello_world():
    user = User.query.all()
    post = Post.query.all()
    for user in user:
        return f'Hello, {user.username}!'

if __name__ == '__main__':
    app.run(port=5000 , debug=True , host='0.0.0.0')
