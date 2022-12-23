from dataclasses import dataclass, field
from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
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

    def _InputField(self, elm: WebElement, value: str):
        """入力バーに要素を入力する"""
        elm.clear()
        elm.send_keys(value)

    def InputFieldByXPATH(self, xpath: str, value: str):
        """xpathを指定して入力バーに入力する"""
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        elm = self.driver.find_element(By.XPATH, xpath)
        self._InputField(elm, value)

    def InputFieldByID(self, id: str, value: str):
        """idを指定して入力バーに入力する"""
        self.wait.until(EC.visibility_of_element_located((By.ID, id)))
        elm = self.driver.find_element(by=By.ID, value=id)
        self._InputField(elm, value)

    def InputFieldByName(self, name: str, value: str):
        """nameを指定して入力バーに入力する"""
        self.wait.until(EC.visibility_of_element_located((By.NAME, name)))
        elm = self.driver.find_element(by=By.NAME, value=name)
        self._InputField(elm, value)


def main():
    driver = DownloadWebDriver()
    url = "https://www.selenium.dev/selenium/web/web-form.html"
    operator = DriverOperator(driver)
    operator.Start(url)
    operator.InputFieldByID("my-text-id", "Text input")
    operator.InputFieldByName("my-password", "Password")
    text_area_xpath = "/html/body/main/div/form/div/div[1]/label[3]/textarea"
    operator.InputFieldByXPATH(text_area_xpath, "Textarea")
    operator.Quit()


if __name__ == "__main__":
    main()
