
from models.db import db


class Vocabularys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    type = db.Column(db.String, nullable=False)
    origin = db.Column(db.String, nullable=False)
    translate = db.Column(db.String, nullable=False)
    progress = db.relationship('Progress')

    # Create function to return String

    def __repr__(self):
        return self.id
