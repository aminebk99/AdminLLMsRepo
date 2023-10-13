from config import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text , nullable=False)
    author_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.title
    