import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def DownloadWebDriver() -> webdriver.Chrome:
    """webdriverをダウンロードする"""

    service = ChromeService(ChromeDriverManager(path=os.getcwd()).install())
    return webdriver.Chrome(service=service)
