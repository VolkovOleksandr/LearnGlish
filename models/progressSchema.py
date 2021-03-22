from models.ma import ma
from models.topic import Topics


class ProgressSchema(ma.Schema):
    class Meta:
        model: Topics
        fields = ("user_id", "id", "topic_id", "vocabulary_id",
                  "last_repeat", "attempts", "success")
