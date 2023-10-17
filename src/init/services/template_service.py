from init import db
from init.models import LLMType, LLMTemplate

class TemplateService:

    def __init__(self, app):
        self.app = app
        self.setup_oauth()

    def setup_oauth(self):
        oauth = OAuth(self.app)
        self.github = oauth.remote_app(
            'github',
            consumer_key=self.app.config['GITHUB_CLIENT_ID'],
            consumer_secret=self.app.config['GITHUB_CLIENT_SECRET'],
            request_token_params={'scope': 'user:email'},
            base_url='https://api.github.com/',
            request_token_url=None,
            access_token_method='POST',
            access_token_url='https://github.com/login/oauth/access_token',
            authorize_url='https://github.com/login/oauth/authorize'
        )

    def loginWithGithub(self):
        return self.authorize_github()

    def authorize_github(self):
        callback_url = url_for('authorized', _external=True)  
        return self.github.authorize(callback=callback_url)

    def get_github_oauth_token(self):
        return session.get('github_token')

    def fetch_github_user_data(self):
        token = self.get_github_oauth_token()
        if token is not None:
            response = self.github.get('user')
            return response.data
        return None

    def handle_github_callback(self):
        response = self.github.authorized_response()
        if response is None or response.get('access_token') is None:
            return jsonify({'error': 'GitHub authorization failed'}), 400  # Return a JSON error response

        session['github_token'] = (response['access_token'], '')
        return redirect(url_for('authenticated'))  # Redirect to a success route

    
