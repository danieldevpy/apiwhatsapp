from abc import ABC, abstractmethod
from src.application.infra.selenium.driver_controller import DriverController

class QrCodeRepository(ABC):

    def __init__(self, driver_controller: DriverController) -> None:
        self.controller = driver_controller

    @abstractmethod
    def get_image(self):
        pass