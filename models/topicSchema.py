from models.ma import ma
from models.topic import Topics


class TopicSchema(ma.Schema):
    class Meta:
        model: Topics
        fields = ("topic",)
