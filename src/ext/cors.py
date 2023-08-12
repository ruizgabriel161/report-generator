from flask_cors import CORS


def init_app(app):
    CORS(app=app, origins=r"https://0a86-191-162-165-120.ngrok-free.app")

