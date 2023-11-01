from ..models import LLMTemplate
from ..database import db
from flask import jsonify

def create_llms(name, description, image_url, type, tags):
    try:
        new_llms = LLMTemplate(name=name, description=description, docker_image_url=image_url, type=type, tags=tags)
        db.session.add(new_llms)
        db.session.commit()
        return jsonify({'message': 'LLMS Template saved successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create LLMS Template'}), 500