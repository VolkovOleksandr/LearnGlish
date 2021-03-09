
from models.db import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    vocabularys = db.relationship('Vocabularys')
    progress = db.relationship('Progress')

    # Create function to return String
    def __repr__(self):
        return self.id
