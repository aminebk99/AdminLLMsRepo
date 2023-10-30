from ..database import db
from enum import Enum
import uuid
from datetime import datetime

class LLMType(Enum):
    OS_LLM = 'OS_LLM'
    Cloud_LLM = 'Cloud_LLM'

class LLMTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    docker_image_url = db.Column(db.String, nullable=False)
    type = db.Column(db.Enum(LLMType), nullable=False, default=LLMType.OS_LLM)  
    uuid = db.Column(db.String, nullable=False, unique=True, default=str(uuid.uuid4()))
    version = db.Column(db.String, nullable=False, default='1.0') 
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    tags = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'docker_image_url': self.docker_image_url,
            'type': self.type.value,
            'uuid': self.uuid,
            'version': self.version,
            'is_active': self.is_active,
            'tags': self.tags,
            'created_at': self.created_at
        }
