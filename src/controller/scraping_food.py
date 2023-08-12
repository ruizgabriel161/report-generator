from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class ScrapingFood:
    """docstring for WebscrapingIfood."""

    def __init__(self):
        self.service = Service(executable_path="K:\Drives\chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service)

        self.wait = WebDriverWait(self.driver, 3)

    def Navigator_Site(self):
        self.driver.get("https://www.ifood.com.br/inicio")
        self.driver.maximize_window()

    def DefinedLocalization(
        self,
        cep: str,
    ):
        self.driver.find_element(
            by=By.XPATH,
            value="/html/body/div[5]/div/div/div/div/div/div[1]/div/div/div[2]/div[1]/button[2]",
        ).click()

        try:
            self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[5]/div/div/div/div/div/div[2]/div/div[1]/div[2]/input",
                    )
                )
            ).send_keys(cep)

            sleep(3)
            self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "/html/body/div[5]/div/div/div/div/div/div[2]/div/div[1]/div[3]/ul/li[1]/div/button",
                    )
                )
            ).click()

        except Exception as e:
            raise e

        sleep(2)
        self.driver.find_element(
            by=By.XPATH, value='//*[@id="addressEmptyNumber"]'
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[5]/div/div/div/div/div/div[2]/div/div[3]/div/form/button",
                )
            )
        ).click()
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[5]/div/div/div/div/div/div[3]/div[2]/button")
            )
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "/html/body/div[5]/div/div/div/div/div/div[3]/div[1]/div[2]/form/div[4]/button",
                )
            )
        ).click()

    def Finder(self, _type: str):
        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="__next"]/div[1]/header/div[2]/form/div/input')
            )
        ).send_keys(f"{_type}\n")

        sleep(3)

    def CaptureLinks(self, limit: int) -> list:
        div_main = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="marmita-panel0-1"]/section/section/article/section[1]/div',
                )
            )
        )

        links = div_main.find_elements(By.CLASS_NAME, "merchant-v2__link")


        limit = limit if limit < 100 else None

        links = [href.get_attribute("href") for href in links[:limit]]

        return links

    def ScrappingInfo(self, links: list) -> pd.DataFrame:
        base = pd.DataFrame(
            columns=["Nome_Ifood", "CEP_Ifood", "Endereço_Ifood", "Cnpj_ifood"]
        )
        for link in links:
            self.driver.get(link)

            sleep(3)

            try:
                nome_ifood = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//*[@id="__next"]/div[1]/main/div[1]/div/header[2]/div[1]/div/div[1]/h1',
                        )
                    )
                ).text

                self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//*[@id="__next"]/div[1]/main/div[1]/div/header[2]/div[1]/div/div[2]/button',
                        )
                    )
                ).click()

                sleep(2)

                infos = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (
                            By.CLASS_NAME,
                            'merchant-details-about__info',
                        )
                    )
                )

                infos = infos[-2:]

                sleep(3)

                endereco = f"{infos[0].find_elements(by=By.CLASS_NAME, value='merchant-details-about__info-data')[0].text}, {infos[0].find_elements(by=By.CLASS_NAME, value='merchant-details-about__info-data')[1].text}"

                cep = (
                    infos[0]
                    .find_elements(
                        by=By.CLASS_NAME, value="merchant-details-about__info-data"
                    )[2]
                    .text
                ).strip()
                cep = cep[cep.find(": ") + 1 :].strip()

                cnpj = (
                    infos[1]
                    .find_elements(
                        by=By.CLASS_NAME, value="merchant-details-about__info-data"
                    )[0]
                    .text
                )

                cnpj = cnpj[cnpj.find(": ") + 1 :].strip()

                base.loc[len(base)] = {
                    "Nome_Ifood": nome_ifood,
                    "CEP_Ifood": cep,
                    "Endereço_Ifood": endereco,
                    "Cnpj_ifood": cnpj,
                }

            except Exception as e:

                print(e)
                return base

        return base


if __name__ == "__main__":
    obj = ScrapingFood()

    obj.Navigator_Site()

    obj.DefinedLocalization("20250001")

    obj.Finder("restaurantes")

    links = obj.CaptureLinks(limit=10)

    df_ifood = obj.ScrappingInfo(links=links)

    df_ifood.to_excel(
        r"K:\Workspace\Python\Report_Generator\sheets\teste_ifood.xlsx", index=False
    )
