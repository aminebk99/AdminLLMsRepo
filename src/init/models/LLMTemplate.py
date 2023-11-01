import uuid
import datetime
from init.database  import db

class LLMTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(70), nullable=False)
    description = db.Column(db.String(200) , nullable=True)
    docker_image_url = db.Column(db.String(200))
    type = db.Column(db.Enum('OS_LLM', 'Cloud_LLM'), default='OS_LLM', nullable=False)
    uuid = db.Column(db.String(36), default=str(uuid.uuid4()), unique=True, nullable=False)
    version = db.Column(db.Float, default=1.0)
    is_active = db.Column(db.Boolean, default=True)
    tags = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'docker_image_url': self.docker_image_url,
            'type': self.type,
            'uuid': self.uuid,
            'version': self.version,
            'is_active': self.is_active,
            'tags': self.tags,
            'created_at': self.created_at
        }
