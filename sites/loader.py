from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from logger import logger


class Loader:
    def __init__(self, *args, **kwargs):
        self.driver = webdriver.Chrome

    def load(self, url: str):
        try:
            self.driver.get(url)
            self.page_source = self.driver.page_source
            return self.page_source
        except Exception as ex:
            logger.error(ex)
            raise ValueError(f"Something went wrong {url=}")

    def __enter__(self):
        service = Service()
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=options)
        # self.driver.set_page_load_timeout(2)
        return self

    def __exit__(self, type, value, traceback):
        self.driver.close()
