from importlib import import_module

from dynaconf import FlaskDynaconf


def load_extensions(app):
    for extension in app.config.EXTENSIONS:

        module_name, factory = extension.split(":")

        ext = import_module(module_name)

        if "socket" in module_name:
            sockeio = getattr(ext, factory)(app)

        try:
            getattr(ext, factory)(app)
        
        except TypeError as e:
            getattr(ext, factory)(app, sockeio)


def init_app(app, **config):
    FlaskDynaconf(app, **config)
