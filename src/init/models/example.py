from init  import db

class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    example = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(120), nullable=False)
