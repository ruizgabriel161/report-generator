
from flask_session import Session


def init_app(app):

    Session(app=app)
