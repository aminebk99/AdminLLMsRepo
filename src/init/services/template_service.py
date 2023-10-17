from init import db
from init.models import LLMType, LLMTemplate
from flask import session, url_for, jsonify, redirect  
from ..config import Config

class TemplateService:
     
    def loginWithGithub(github):
        callback_url = url_for('authorized', _external=True)
        return github.authorize_redirect(callback=callback_url)
    
