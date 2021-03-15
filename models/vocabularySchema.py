from models.ma import ma
from models.vocabulary import Vocabularys


class VocabularySchema(ma.Schema):
    class Meta:
        model: Vocabularys
        fields = ("id", "user_id", "topic_id", "type", "origin", "translate")
