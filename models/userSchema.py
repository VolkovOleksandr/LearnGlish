from models.ma import ma
from models.user import Users


class UserSchema(ma.Schema):
    class Meta:
        model: Users
        fields = ("name", "id", "email", "password")
