
from models.db import db
topic_identifier = db.Table('topic_identifier',
                            db.Column('user_id', db.Integer,
                                      db.ForeignKey('users.id')),
                            db.Column('topic_id', db.Integer,
                                      db.ForeignKey('topics.id'))
                            )


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    vocabularys = db.relationship('Vocabularys')
    progress = db.relationship('Progress')
    topics = db.relationship('Topics', secondary=topic_identifier)
    # Create function to return String

    def __repr__(self):
        return self.id
