from flask import Flask

from src.ext import configuration


def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)
    return app


def create_app(environ, start_response, **config):

    app = minimal_app(**config)

    socket_istance = configuration.load_extensions(app)
    socket_istance.run(host='0.0.0.0', port=10000)
    return app(environ=environ, start_response=start_response)
