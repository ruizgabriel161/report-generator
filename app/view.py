import os
import random
from time import sleep

from flask import Flask, jsonify, render_template, request, send_file

from app import app
from app.info_maps import StartMaps

template_dir = os.path.join(os.path.dirname(__file__), "templates")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        render_template("index.html", status="Gerando relatório. Por favor aguarde")

        filename = os.path.join(
            os.path.dirname(__file__), os.pardir, "sheets", "teste.csv"
        )

        objStart = StartMaps(request.form.get("tipo"))
        ids = objStart.definedIds(request.form.get("cep"))

        df = objStart.findInfo(ids=ids)

        result = objStart.exportDataFrame(filename=filename, df=df)

        if result:
            try:
                return send_file(filename, as_attachment=True)

            except Exception as e:
                render_template("index.html", status="Erro ao gerar o relatório.")

    return render_template("index.html")
