import datetime
from dataclasses import InitVar, dataclass, field
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

    def _InputField(self, elm: WebElement, value: str):
        """入力バーに要素を入力する"""
        elm.clear()
        elm.send_keys(value)

    def InputFieldByXPATH(self, xpath: str, value: str):
        """xpathを指定して入力バーに入力する"""
        self.web.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        elm = self.web.driver.find_element(By.XPATH, xpath)
        self._InputField(elm, value)

    def InputFieldByID(self, id: str, value: str):
        """idを指定して入力バーに入力する"""
        self.web.wait.until(EC.visibility_of_element_located((By.ID, id)))
        elm = self.web.driver.find_element(by=By.ID, value=id)
        self._InputField(elm, value)

    def InputFieldByName(self, name: str, value: str):
        """nameを指定して入力バーに入力する"""
        self.web.wait.until(EC.visibility_of_element_located((By.NAME, name)))
        elm = self.web.driver.find_element(by=By.NAME, value=name)
        self._InputField(elm, value)

    def SelectDropDownMenu(self, xpath: str, select_value: str):
        """ドロップダウンメニュー(select)をクリックして、指定した要素を選択する"""
        self.web.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        dropdown = self.web.driver.find_element(by=By.XPATH, value=xpath)
        Select(dropdown).select_by_visible_text(select_value)

    def SelectDropDownMenuFromDataList(self, xpath: str, select_value: str):
        """ドロップダウンメニュー(datalist)をクリックして、指定した要素を選択する"""
        self.web.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        datalist = self.web.driver.find_element(by=By.XPATH, value=xpath)
        datalist.send_keys(select_value)

    def EnableCheckBox(self, xpath: str):
        """チェックボックスにチェックを付ける"""
        self.web.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        checkbox = self.web.driver.find_element(by=By.XPATH, value=xpath)
        if not checkbox.is_selected():
            checkbox.click()


def main():
    chrome_wnd = ChromeWindow(WebDriverWindow(DownloadWebDriver()))
    url = "https://www.selenium.dev/selenium/web/web-form.html"
    chrome_wnd.Start(url)
    chrome_wnd.InputFieldByID("my-text-id", "Text input")
    chrome_wnd.InputFieldByName("my-password", "Password")
    text_area_xpath = "/html/body/main/div/form/div/div[1]/label[3]/textarea"
    chrome_wnd.InputFieldByXPATH(text_area_xpath, "Textarea")
    drop_down_menu = "/html/body/main/div/form/div/div[2]/label[1]/select"
    chrome_wnd.SelectDropDownMenu(drop_down_menu, "Two")
    datalist_xpath = "/html/body/main/div/form/div/div[2]/label[2]/input"
    chrome_wnd.SelectDropDownMenuFromDataList(datalist_xpath, "New York")
    enabled_checkbox = "/html/body/main/div/form/div/div[2]/div[1]/label[1]/input"
    disabled_checkbox = "/html/body/main/div/form/div/div[2]/div[1]/label[2]/input"
    chrome_wnd.EnableCheckBox(enabled_checkbox)
    chrome_wnd.EnableCheckBox(disabled_checkbox)
    date_picker = "/html/body/main/div/form/div/div[3]/label[2]/input"
    today = datetime.datetime.now().strftime("%m/%d/%Y")
    chrome_wnd.InputFieldByXPATH(date_picker, today)
    sleep(5)  # Debug
    chrome_wnd.Quit()


if __name__ == "__main__":
    main()
