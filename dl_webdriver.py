import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def DownloadWebDriver() -> webdriver.Chrome:
    """webdriverをダウンロードして、ダウンロードしたdriverを返す"""

    service = ChromeService(ChromeDriverManager(path=os.getcwd()).install())
    return webdriver.Chrome(service=service)
