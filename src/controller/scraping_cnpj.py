import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


class ScrapingCNPJ:
    """docstring for ScrappingCNPJ."""

    def __init__(self, df: pd.DataFrame):

        self.df: pd.DataFrame = self.treatBase(df=df)
        self.cnpjs: list = [
            re.sub("\D", "", number) for number in self.df["Cnpj_ifood"].tolist()
        ]

    def treatBase(self, df: pd.DataFrame) -> pd.DataFrame:

        print(df.columns)

        df = df.drop_duplicates(subset=["Cnpj_ifood"], keep="first").reset_index(
            drop=True
        )

        return df

    def decode_cfemail(self, encoded_email):
        pairs = [encoded_email[i : i + 2] for i in range(0, len(encoded_email), 2)]

        # Decodificando o email
        decoded_email = ""
        key = int(pairs[0], 16)
        for pair in pairs[1:]:
            decoded_email += chr(int(pair, 16) ^ key)

        return decoded_email

    def scrapping(self):

        df_base = self.df
        contents = [
            "Logradouro",
            "Bairro",
            "Município",
            "Estado",
            "Telefone(s)",
            "E-mail",
        ]

        i = 0
        for cnpj in self.cnpjs:
            response = requests.get(f"https://cnpj.biz/{cnpj}")

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                for content in contents:
                    element = soup.find(
                        lambda tag: tag.name == "p" and content in tag.text
                    )

                    if content == "E-mail":
                        if element != None:
                            data_cfemail_value = element.find(
                                "a", {"data-cfemail": True}
                            )["data-cfemail"]

                            value = self.decode_cfemail(data_cfemail_value)

                    else:
                        value = (
                            element.get_text()[
                                element.get_text().find(": ") + 1 :
                            ].strip()
                            if element != None
                            else ""
                        )

                    df_base.loc[i, content] = value

                i += 1

                print(df_base)

        return df_base


if __name__ == "__main__":
    objCnpj = ScrapingCNPJ(df=pd.read_excel(r"sheets\teste_ifood.xlsx"))
    df = objCnpj.scrapping()

    df.to_excel(r"sheets\teste_cnpj.xlsx", index=False)
