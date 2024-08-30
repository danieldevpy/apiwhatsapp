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
            except:
                print('Tentativa', t)

    return wrapper

class WhatsappController(WhatsappRepository):

    def __init__(self, driver_controller: DriverController) -> None:
        self.driver_controller = driver_controller

    def send_message(self, message: Message):
        self.__open_new_contact__(message.number)
        self.__write_message__(message.message)
        self.__get_last_message__(message.message)

    @retry
    def __open_new_contact__(self, number: str):
        self.driver_controller.click_element(elements.input_for_new_conversations)
        input_active = self.driver_controller.get_element_active()
        input_active.send_keys(number)
        self.driver_controller.await_element(elements.info_not_in_list_contact)
        input_active.send_keys(Keys.ENTER)

    @retry
    def __write_message__(self, message: str):
        self.driver_controller.set_value(elements.input_write_message, message, True)
    
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
        if not last_element.text == message:
            raise Exception("Algum erro ao validar a mensage")

    
    
