from abc import ABC, abstractmethod
from src.domain.entity.message import Message

class WhatsappRepository(ABC):

    @abstractmethod
    def send_message(self, message: Message):
        raise NotImplemented
    

