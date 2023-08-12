from time import sleep

import openpyxl
import pandas as pd
import requests


class InfoMaps:
    """Busca Informações no maps"""

    def __init__(self, api_key: str, search: str):
        self.api_key = api_key
        self.search = search

    def Results(
        self, url: str, params: dict, columns: list, df_base=None
    ) -> pd.DataFrame:
        if df_base is None:
            df_base = pd.DataFrame()

        # Faça a solicitação HTTP à API Places
        response = requests.get(url, params=params)

        # Verifique se a solicitação foi bem-sucedida
        if response.status_code == requests.codes.ok:
            # Extraia informações dos resultados
            data = response.json()

            if df_base.empty:
                if "place_id" in columns:
                    all_results: list[dict] = []
                    while True:
                        result = data["results"]
                        all_results.extend(result)

                        if "next_page_token" not in data:
                            break

                        sleep(2)

                        params["pagetoken"] = data["next_page_token"]

                        response = requests.get(url, params=params)
                        data = response.json()

                    df_base = pd.DataFrame(all_results)
                else:
                    result = data["result"]

                    results = {key: result.get(key, "Não informado") for key in columns}

                    df_base = pd.DataFrame(results, index=[0], columns=columns)

            else:
                result = data["result"]

                results = {key: result.get(key, "Não informado") for key in columns}

                new_row = pd.DataFrame(results, index=[0])

                df_base = pd.concat([df_base, new_row], ignore_index=True)

        else:
            return False

        return df_base

    def DefinedCoordinates(self, address: str, url: str):
        params_requests = {"address": address, "key": self.api_key}

        response = requests.get(url=url, params=params_requests)

        data = response.json()

        if data["status"] == "OK":
            results = data["results"]

            latitude = results[0]["geometry"]["location"]["lat"]
            longitude = results[0]["geometry"]["location"]["lng"]

            return f"{latitude},{longitude}"
        else:
            return False


class StartMaps(InfoMaps):
    """Classe filha da InfoMaps"""

    URL_LAT_LONG = r"https://maps.googleapis.com/maps/api/geocode/json"
    URL_DETAILS = r"https://maps.googleapis.com/maps/api/place/details/json"
    URL_SEARCH = r"https://maps.googleapis.com/maps/api/place/textsearch/json"

    def __init__(self, api_key: str, search: str):
        super().__init__(api_key=api_key, search=search)

    def definedIds(self, address):
        lat_long = super().DefinedCoordinates(
            address=address, url=StartMaps.URL_LAT_LONG
        )

        params = {
            "location": lat_long,
            "radius": 5,  # Raio de busca em metros
            "query": self.search,  # Tipo de estabelecimento (empresa)
            "key": self.api_key,
        }

        df = super().Results(
            url=StartMaps.URL_SEARCH, columns=["place_id"], params=params
        )

        if df is not False:
            ids = df["place_id"].values.tolist()

            return ids
        else:
            return False

    def findInfo(self, ids: list, df_base=None, limit=None):
        if df_base is None:
            df_base = pd.DataFrame()

        if limit is not None:
            ids = ids[:limit]

        for id in ids:
            params = {"place_id": id, "key": self.api_key}

            try:
                df_base = super().Results(
                    url=StartMaps.URL_DETAILS,
                    columns=[
                        "name",
                        "formatted_address",
                        "formatted_phone_number",
                        "rating",
                        "website",
                    ],
                    df_base=df_base,
                    params=params,
                )

            except Exception as e:
                print(e)
                continue

        return df_base

    def exportDataFrame(self, filename, df: pd.DataFrame):
        try:
            df = df.rename(
                columns={
                    "name": "Nome",
                    "formatted_address": "Endereco",
                    "formatted_phone_number": "Telefone",
                    "rating": "Avaliação",
                }
            )

        finally:
            try:
                df.to_excel(filename, index=False)

                return True
            except Exception as e:
                print(e)
                return False


if __name__ == "__main__":
    objStart = StartMaps("Veterinária")
    ids = objStart.definedIds("20250-001")

    df = objStart.findInfo(ids=ids)
    result = objStart.exportDataFrame("teste.csv", df=df)
