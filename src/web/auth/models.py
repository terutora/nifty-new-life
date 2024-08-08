from flask_login import UserMixin

from ..models import DB


class User(DB.Model, UserMixin):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(128), unique=True)
    hashed_password = DB.Column(DB.String(256))
    professional = DB.Column(DB.Integer, DB.ForeignKey("professional.professional_id"))

    def __init__(self, username: str, hashed_password: str, professional: int):
        self.username = username
        self.hashed_password = hashed_password
        self.professional = professional
