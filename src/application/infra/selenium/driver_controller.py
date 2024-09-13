from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from src.domain.entity.element import Element
import shutil, time

class DriverController:

    def __init__(self, url: str, hadless=False, cache=False, remove_data=False) -> None:
        if remove_data:
            shutil.rmtree('~')
            time.sleep(1)
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        if hadless:
            chrome_options.add_argument("--headless=new")
        if cache:
            chrome_options.add_argument('--user-data-dir=~/.config/google-chrome')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        self.driver.get(url)

    def get_element(self, element: Element):
        try:
            return WebDriverWait(self.driver, element.time).until(
            EC.visibility_of_element_located((element.type, element.element_search))
            )
        except:
            if not element.element_retry:
                raise Exception(f'Elemento {element.name} não encontrado')
            return self.get_element(element.element_retry)

    def get_elements(self, element: Element):
        try:
           return WebDriverWait(self.driver, element.time).until(
            EC.visibility_of_all_elements_located((element.type, element.element_search))
            )
        except:
            raise Exception(f'Elemento {element.name} não encontrado')

    def set_value(self, element: Element, value: str, confirm=False):
        element_html = self.get_element(element)
        if confirm:
            element_html.send_keys(value, Keys.ENTER)
        else:
            element_html.send_keys(value)

    def click_element(self, element: Element):
        element_html = self.get_element(element)
        element_html.click()

    def get_element_active(self):
        return self.driver.execute_script("return document.activeElement")

    def await_element(self, element: Element):
        try:
            WebDriverWait(self.driver, element.time).until(
                EC.visibility_of_element_located((element.type, element.element_search))
            )
        except:
            raise Exception(f'Elemento {element.name} não apareceu na pagina')
        


