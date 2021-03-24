from models.ma import ma
from models.news import News


class NewsSchema(ma.Schema):
    class Meta:
        model: News
        fields = ("title", "id", "text", "user_id")
