from src.application.infra.selenium.driver_controller import DriverController
from src.application.repository.wpp_repository import WhatsappRepository
from src.domain.entity.message import Message
from src.application.infra.selenium import elements
from selenium.webdriver.common.keys import Keys
import time

def retry(fun):
    def wrapper(self, *args, **kwargs):
        for t in range(1, 4):
            try:
                fun(self, *args, **kwargs)
                break
            except Exception as e:
                if t == 3:
                    raise Exception(f"Tentativa máxima excedida na função '{fun.__name__}'!\n" + str(e))

    return wrapper

class WhatsappController(WhatsappRepository):

    def __init__(self, driver_controller: DriverController) -> None:
        self.driver_controller = driver_controller

    def send_message(self, message: Message):
        try:
            self.__open_new_contact__(message.number)
            self.__write_message__(message.message)
            self.__esc__()
        except Exception as e:
            self.__esc__()
            raise e

    @retry
    def __open_new_contact__(self, number: str):
        try:
            element_search = elements.Element("teste", f'._ak8q span[title="{number}"]', elements.By.CSS_SELECTOR)
            try:
                element = self.driver_controller.get_element(element_search)
            except:
                self.driver_controller.click_element(elements.input_for_new_conversations)
                input_active = self.driver_controller.get_element_active()
                input_active.send_keys(number)
                element = self.driver_controller.get_element(element_search)
            finally:
                element.click()
        except Exception as e:
            self.__esc__()
            raise e

    @retry
    def __write_message__(self, message: str):
        input = self.driver_controller.get_element(elements.input_write_message)
        if input.text:
            for _ in range(len(input.text)):
                input.send_keys(Keys.BACK_SPACE)
        input.send_keys(message, Keys.ENTER)

    @retry
    def __get_messages__(self):
        message_elements = self.driver_controller.get_elements(elements.messages_conversation)
        if not message_elements:
            raise Exception("Messages não encontadas")
        return message_elements

    @retry
    def __get_last_message__(self, message: str):
        message_elements = self.driver_controller.get_elements(elements.messages_conversation)
        last_element = message_elements[-1]
        if not last_element.text in message:
            raise Exception("Algum erro ao validar a mensage")
    
    def __esc__(self):
        body = self.driver_controller.get_element(elements.body)
        body.click()
        body.send_keys(Keys.ESCAPE)


    
    
