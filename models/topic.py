
from models.db import db


class Topics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String, nullable=False, unique=True)
    vocabularys = db.relationship('Vocabularys')
    progress = db.relationship('Progress')

    # Create function to return String
    def __repr__(self):
        return self.id
