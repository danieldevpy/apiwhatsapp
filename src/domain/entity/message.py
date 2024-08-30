from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class Message:
    number: str
    message: str

class RequestMessage(BaseModel):
    number: str
    message: str

    def create_message(self):
        return Message(self.number, self.message)