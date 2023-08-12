from flask_socketio import SocketIO


def init_app(app):
    socketio = SocketIO(app=app)
    return socketio



  
