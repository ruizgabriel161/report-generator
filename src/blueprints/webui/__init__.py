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


bp.add_url_rule("/webui/login", view_func=index)
bp.add_url_rule("/webui/maps", view_func=index)
bp.add_url_rule("/webui/food", view_func=index)
bp.add_url_rule("/webui/init", view_func=page_first)


bp.add_url_rule("/webui/logout", view_func=logout)

bp.add_url_rule(
    "/webui/status/<socketid>/<_type>/<cep>/<uri>", view_func=status, methods=["POST"]
)
bp.add_url_rule(
    "/webui/register_user/<socketid>/<user>/<password>",
    view_func=register_user,
    methods=["POST"],
)

bp.add_url_rule("/webui/download/<uri>", view_func=download, methods=["GET"])

def page(app):

    @app.errorhandler(404)
    def page_not_found(error):
        return redirect("/login")

def init_app(app, socketio):
    app.register_blueprint(bp, url_prefix="/webui")
    bp.socketio = socketio
    page(app=app)
