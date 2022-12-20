from dataclasses import dataclass, field

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from dl_webdriver import DownloadWebDriver


@dataclass
class DriverOperator:
    driver: WebDriver
    wait: WebDriverWait = field(init=False)

    def __post_init__(self):
        self.wait = WebDriverWait(self.driver, timeout=10)

    def Start(self, url: str):
        """受け取ったURL先にアクセスする"""
        self.driver.get(url)

    def Quit(self):
        """WebDriverを閉じる"""
        self.driver.quit()


def main():
    driver = DownloadWebDriver()
    url = "https://www.selenium.dev/selenium/web/web-form.html"
    operator = DriverOperator(driver)
    operator.Start(url)
    operator.Quit()


if __name__ == "__main__":
    main()
