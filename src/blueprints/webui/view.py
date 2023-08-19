import io
import os

import requests
from flask import (
    Response,
    after_this_request,
    current_app,
    redirect,
    render_template,
    request,
    send_file,
    session,
)

from src.controller.defined_action import DefinedAction
from src.controller.info_maps import StartMaps
from src.ext import configuration, socket
from src.ext.auth import create_user, seach_signature, verify_login, verify_permission



def page_first():

    return render_template("page_first.html")

def index():
    socketio = current_app.extensions["socketio"]

    uri = request.full_path.replace("?", "")

    socket_url = request.host_url[:-1]

    print(socket_url)

    match uri:
        case "/maps":
            if "username" not in session or not verify_permission(
                user=session["username"], uri=uri
            ):
                return redirect("/login")
            return render_template(
                "index.html",
                Title="Obter lista de estabelecimentos",
                label1="CEP",
                label2="Tipo",
                title_button="Gerar",
                link_download="/download/maps",
                route=uri,
                socket_url=socket_url
            )
        case "/food":
            
            if "username" not in session or not verify_permission(
                user=session["username"], uri=uri
            ):
                return redirect("/login")
            return render_template(
                "index.html",
                Title="Obter lista de estabelecimentos",
                label1="CEP",
                label2="Tipo",
                title_button="Gerar",
                link_download="/download/food",
                route=uri,
                socket_url=socket_url
            )

        case "/login":
            return render_template(
                "index.html",
                Title="Login",
                label1="Login",
                label2="Senha",
                title_button="Entrar",
                route=uri,
                socket_url=socket_url
            )


async def status(socketid, _type, cep, uri):
    uri = str(uri).strip()
    KEY = current_app.config.API_KEY
    socketio = current_app.extensions["socketio"]

    if request.method == "POST":
        match uri:
            case "maps":
                if "username" not in session or not verify_permission(
                    user=session["username"], uri=uri
                ):
                    socketio.emit("redirect", "/login", to=socketid)
                    return Response(status=204)
                socketio.emit(
                    "status", "Processando o dados. Por favor Aguarde", to=socketid
                )

                objDefined = DefinedAction(
                    "maps",
                    socketio=socketio,
                    socketid=socketid,
                    _type=_type,
                    cep=cep,
                    key_maps=KEY,
                    username=session["username"],
                )

            case "food":
                if "username" not in session or not verify_permission(
                    user=session["username"], uri=uri
                ):
                    socketio.emit("redirect", "/login", to=socketid)
                    return Response(status=204)

                socketio.emit(
                    "status", "Processando o dados. Por favor Aguarde", to=socketid
                )

                objDefined = DefinedAction(
                    "food",
                    socketio=socketio,
                    socketid=socketid,
                    _type=_type,
                    cep=cep,
                    key_maps=KEY,
                    username=session["username"],
                )

            case "login":
                user = {
                    "username": cep,
                    "password": _type,
                }

                session["username"] = cep

                session["_permanent"] = False

                login = verify_login(user=user)

                signature = seach_signature(user=cep)

                if login:
                    socketio.emit("redirect", f"/{signature}", to=socketid)
                else:
                    socketio.emit("status", "login inválido", to=socketid)

    return Response(status=204)


def logout(socketid):
    session.pop("username", None)

    return redirect("/login")


async def register_user(socketid, user, password):
    response = create_user(username=user, password=password)
    socketio = current_app.extensions["socketio"]
    socketio.emit("status_register", response, to=socketid)

    return response


def download(uri):
    folder_sheets = os.path.join(os.path.abspath(os.getcwd()), "sheets")

    match uri:
        case "maps":
            filename = r"maps " + session["username"] + ".xlsx"

            full_filename = os.path.join(folder_sheets, filename)

        case "food":
            filename = r"\food " + session["username"] + ".xlsx"

            full_filename = os.path.join(folder_sheets, filename)

    @after_this_request
    def delete_file(response):
        try:
            os.remove(full_filename)
            response.direct_passthrough = False
        except Exception as ex:
            print(ex)
        return response

    with open(full_filename, "rb") as file:
        file_content = file.read()

    response = send_file(
        io.BytesIO(file_content),
        as_attachment=True,
        download_name=filename,
    )

    response.direct_passthrough = True

    return response

