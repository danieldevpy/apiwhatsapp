from src.application.repository.wpp_repository import WhatsappRepository
from src.domain.entity.message import Message


def send_message_wpp(repository: WhatsappRepository, message: Message):
    if message.number == 'Ti Cisbaf':
        message.number = 'TI Cisbaf'
        return repository.send_message(message)
    elif len(message.number) != 11:
        raise Exception("Número incorreto!")
    elif len(message.message) <= 0:
        raise Exception("Envie alguma mensagem")
    else:
        message.number = f'+55 {message.number[:2]} {message.number[2:7]}-{message.number[7:]}'
        return repository.send_message(message)