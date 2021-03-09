from datetime import datetime

from models.db import db


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    vocabulary_id = db.Column(db.Integer, db.ForeignKey('vocabularys.id'))
    last_repeat = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    attempts = db.Column(db.Integer, nullable=False, default=0)
    sucsses = db.Column(db.Integer, nullable=False, default=0)

    # Create function to return String

    def __repr__(self):
        return self.id
