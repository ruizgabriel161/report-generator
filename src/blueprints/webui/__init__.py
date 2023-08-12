from flask import Blueprint, redirect, url_for

from .view import (
    download,

    index,
    logout,
    register_user,
    status,
    page_first
)

bp = Blueprint(
    "webui",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/webui/static",
)


bp.add_url_rule("/login", view_func=index)
bp.add_url_rule("/maps", view_func=index)
bp.add_url_rule("/food", view_func=index)
bp.add_url_rule("/init", view_func=page_first)


bp.add_url_rule("/logout", view_func=logout)

bp.add_url_rule(
    "/status/<socketid>/<_type>/<cep>/<uri>", view_func=status, methods=["POST"]
)
bp.add_url_rule(
    "/register_user/<socketid>/<user>/<password>",
    view_func=register_user,
    methods=["POST"],
)

bp.add_url_rule("/download/<uri>", view_func=download, methods=["GET"])

def page(app):

    @app.errorhandler(404)
    def page_not_found(error):
        return redirect("/login")

def init_app(app, socketio):
    app.register_blueprint(bp)
    bp.socketio = socketio
    page(app=app)
