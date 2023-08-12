import re
from logging import error

from flask import request, send_file

from src.controller.info_maps import StartMaps
from src.controller.scraping_cnpj import ScrapingCNPJ
from src.controller.scraping_food import ScrapingFood
from src.models import User


class DefinedAction(object):
    """docstring for DefinedAction."""

    def __init__(self, action, socketio, socketid, _type, cep, key_maps, username):
        self.action = action
        self.socketio = socketio
        self.socketid = socketid
        self._type = _type
        self.cep = cep
        self.key_maps = key_maps
        self.username = username
        self.limit = self.definedLimit()
        self.defineFunction()

    def defineFunction(self):
        match self.action:
            case "maps":
                self.generatorMaps()

            case "food":
                self.generatorFood()

            case _:
                return "Ação Inexistente"

    def definedLimit(self):
        existing_user = User.query.filter_by(username=self.username).first()
        limit = None if existing_user.signature != "freemium" else 5
        return limit

    def generatorMaps(self):
        self.socketio.emit(
            "status", "Processando o dados. Por favor Aguarde", to=self.socketid
        )

        filename = r"sheets\maps " + self.username + ".xlsx"

        try:
            objStart = StartMaps(api_key=self.key_maps, search=self._type)
            ids = objStart.definedIds(self.cep)

            df = objStart.findInfo(ids=ids, limit=self.limit)

            result = objStart.exportDataFrame(filename=filename, df=df)

        except Exception as e:
            print(e)
            self.socketio.emit(
                "status", f"Erro ao gerar o Arquivo {e} ", to=self.socketid
            )

        if result:
            try:
                self.socketio.emit("status", "Arquivo Gerado.", to=self.socketid)
                print("maps2")

                self.socketio.emit(
                    "download_file",
                    request.host_url + "/download/maps",
                    to=self.socketid,
                )

            except Exception as e:
                print(e)
                self.socketio.emit(
                    "status", f"Erro ao gerar o Arquivo {e} ", to=self.socketid
                )

    def generatorFood(self):
        try:
            obj_food = ScrapingFood()

            obj_food.Navigator_Site()

            cep = re.sub(r"\D", "", self.cep)

            obj_food.DefinedLocalization(cep=cep)

            obj_food.Finder(_type=self._type)

            links = obj_food.CaptureLinks(limit=self.limit)

            df_ifood = obj_food.ScrappingInfo(links=links)

            objCnpj = ScrapingCNPJ(df=df_ifood)

            df = objCnpj.scrapping()

            df.to_excel(r"sheets\food " + self.username + ".xlsx", index=False)

            self.socketio.emit("status", "Arquivo Gerado.", to=self.socketid)

            self.socketio.emit(
                "download_file", request.host_url + "download/food", to=self.socketid
            )

        except Exception as e:
            self.socketio.emit(
                "status", f"Erro ao gerar o Arquivo {e} ", to=self.socketid
            )
