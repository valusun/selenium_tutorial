import datetime
from dataclasses import InitVar, dataclass, field
import json
from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from dl_webdriver import DownloadWebDriver


@dataclass
class WebDriverWindow:
    driver: WebDriver
    wait: WebDriverWait = field(init=False)
    time_out: InitVar[float] = 10

    def __post_init__(self, time_out):
        self.wait = WebDriverWait(self.driver, timeout=time_out)


@dataclass
class ChromeWindow:
    web: WebDriverWindow

    def Start(self, url: str):
        """受け取ったURL先にアクセスする"""
        self.web.driver.get(url)

    def Quit(self):
        """WebDriverを閉じる"""
        self.web.driver.quit()

    def _GetElm(self, locator: tuple[str, str]):
        """見つかった属性を返す"""
        self.web.wait.until(EC.visibility_of_element_located(locator))
        return self.web.driver.find_element(*locator)

    def _InputField(self, elm: WebElement, value: str):
        """入力バーに要素を入力する"""
        elm.clear()
        elm.send_keys(value)

    def InputFieldByXPATH(self, xpath: str, value: str):
        """xpathを指定して入力バーに入力する"""
        self._InputField(self._GetElm((By.XPATH, xpath)), value)

    def InputFieldByID(self, id: str, value: str):
        """idを指定して入力バーに入力する"""
        self._InputField(self._GetElm((By.ID, id)), value)

    def InputFieldByName(self, name: str, value: str):
        """nameを指定して入力バーに入力する"""
        self._InputField(self._GetElm((By.NAME, name)), value)

    def SelectDropDownMenuBySelect(self, xpath: str, select_value: str):
        """ドロップダウンメニュー(select)をクリックして、指定した要素を選択する"""
        dropdown = self._GetElm((By.XPATH, xpath))
        Select(dropdown).select_by_visible_text(select_value)

    def SelectDropDownMenuByDataList(self, xpath: str, select_value: str):
        """ドロップダウンメニュー(datalist)をクリックして、指定した要素を選択する"""
        datalist = self._GetElm((By.XPATH, xpath))
        datalist.send_keys(select_value)

    def EnableCheckBox(self, xpath: str):
        """チェックボックスにチェックを付ける"""
        checkbox = self._GetElm((By.XPATH, xpath))
        if not checkbox.is_selected():
            checkbox.click()

    def ClickSubmit(self, xpath: str):
        """Submitボタンを押す"""
        self._GetElm((By.XPATH, xpath)).click()


def GetXPATH():
    """jsonファイルからxpathを取得する"""
    with open("xpath.json", encoding="utf-8") as f:
        xpath = json.load(f)
    return xpath


def main():
    chrome_wnd = ChromeWindow(WebDriverWindow(DownloadWebDriver()))
    url = "https://www.selenium.dev/selenium/web/web-form.html"
    xpath = GetXPATH()
    chrome_wnd.Start(url)
    chrome_wnd.InputFieldByID("my-text-id", "Text input")
    chrome_wnd.InputFieldByName("my-password", "Password")
    chrome_wnd.InputFieldByXPATH(xpath["text_area_xpath"], "Textarea")
    chrome_wnd.SelectDropDownMenuBySelect(xpath["drop_down_menu"], "Two")
    chrome_wnd.SelectDropDownMenuByDataList(xpath["datalist_xpath"], "New York")
    chrome_wnd.EnableCheckBox(xpath["enabled_checkbox"])
    chrome_wnd.EnableCheckBox(xpath["disabled_checkbox"])
    today = datetime.datetime.now().strftime("%m/%d/%Y")
    chrome_wnd.InputFieldByXPATH(xpath["date_picker"], today)
    sleep(5)  # Debug
    chrome_wnd.ClickSubmit(xpath["submit_btn"])
    sleep(5)  # Debug
    chrome_wnd.Quit()


if __name__ == "__main__":
    main()
