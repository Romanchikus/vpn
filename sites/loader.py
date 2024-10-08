import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

from logger import logger


class Loader:
    def __init__(self, absolute_url: str, site_url: str, *args, **kwargs):
        self.driver = webdriver.Chrome
        self.absolute_url = (
            absolute_url[:-1] if absolute_url[-1] == "/" else absolute_url
        )
        self.site_url = site_url[:-1] if site_url[-1] == "/" else site_url
        self.total_MB: float = 0
        self.page_source = None
        logger.info(f"Init with: {self.absolute_url=}, {self.site_url=}")

    def load(self, endpoint: str):
        try:
            url = self.site_url + "/" + endpoint
            self.driver.get(url)
            self.change_internal_links()
        except Exception as ex:
            logger.error(ex)
            raise ValueError(f"Something went wrong {url=}")
        finally:
            total_bytes = []
            for entry in self.driver.get_log("performance"):
                if "Network.dataReceived" in str(entry):
                    r = re.search(r"encodedDataLength\":(.*?),", str(entry))
                    total_bytes.append(int(r.group(1)))
            self.total_MB = round((float(sum(total_bytes) / 1000) / 1000), 2)
            if self.page_source:
                return self.page_source
            return None

    def change_internal_links(self):
        soup = BeautifulSoup(self.driver.page_source, features="lxml")
        for a in soup.findAll("a"):
            route = None
            if a.get("href"):
                if a.get("href")[0] == "/":
                    a["href"] = self.absolute_url + a.get("href")
                    continue
                splitted_link = a.get("href").split(self.site_url)

                if self.site_url == a.get("href"):
                    a["href"] = self.absolute_url
                    continue
                # print(a.get("href"), splitted_link)

                if splitted_link and len(splitted_link) >= 2:
                    if not splitted_link[1]:
                        route = ""
                    else:
                        route = splitted_link[1]

                if route:
                    a["href"] = f"{self.absolute_url}{route}"
        self.page_source = str(soup)

    def __enter__(self):
        options = webdriver.ChromeOptions()
        options.set_capability("goog:loggingPrefs", {"performance": "INFO"})
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--headless')
        self.driver = webdriver.Remote("http://chrome:4444/wd/hub", options=options)
        return self

    def __exit__(self, type, value, traceback):
        self.driver.quit()
