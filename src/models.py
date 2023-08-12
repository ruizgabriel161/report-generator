from sqlalchemy_serializer import SerializerMixin

from src.ext.database import db


class User(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(140), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    signature = db.Column(db.String(20), nullable=True)
