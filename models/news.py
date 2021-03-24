
from models.db import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String, nullable=False, unique=True)
    text = db.Column(db.String, nullable=False)
    # Create function to return String

    def __repr__(self):
        return self.id
