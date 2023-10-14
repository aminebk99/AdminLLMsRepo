from init  import db

class LLMTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    docker_image_url = db.Column(db.String, nullable=False)
    type = db.Column(db.Enum(LLMType), nullable=False)
    uuid = db.Column(db.String, nullable=False, unique=True, default=str(uuid.uuid4()))
    version = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    tags = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)