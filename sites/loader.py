from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

from logger import logger


class Loader:
    def __init__(self, absolute_url: str, *args, **kwargs):
        self.driver = webdriver.Chrome
        self.absolute_url = absolute_url

    def load(self, url: str):
        try:
            self.driver.get(url)
            self.page_source = self.driver.page_source
            self.change_internal_links()
            return self.page_source
        except Exception as ex:
            logger.error(ex)
            raise ValueError(f"Something went wrong {url=}")

    def change_internal_links(self):
        soup = BeautifulSoup(self.page_source, features="lxml")
        for a in soup.findAll("a"):
            internal_link = a.get("href")
            if internal_link:
                a["href"] = f"{self.absolute_url}?orig_url={internal_link}"
        self.page_source = str(soup)

    def __enter__(self):
        service = Service()
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=options)
        # self.driver.set_page_load_timeout(2)
        return self

    def __exit__(self, type, value, traceback):
        self.driver.close()
