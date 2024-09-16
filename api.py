from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from src.application.infra.selenium.driver_controller import DriverController
from src.application.infra.selenium.wpp_controller import WhatsappController
from src.application.usecase import wpp_case
from src.domain.entity.message import RequestMessage
from src.application.infra.selenium.qrcode_controller import QrCodeController
import threading

app = FastAPI()
driver_controller = DriverController('https://web.whatsapp.com/', cache=True, hadless=False)
qr_code = False
message_lock = threading.Lock()  # Cria um lock para controlar o acesso

@app.post('/notification/wpp')
def send_message(request: RequestMessage):
    global qr_code
    if qr_code:
        return Response(content='Qr code não confirmado', status_code=400)
    
    with message_lock:
        try:
            repository = WhatsappController(driver_controller)
            wpp_case.send_message_wpp(repository, request.create_message())
            return JSONResponse({"msg": "Operação bem-sucedida"})
        except Exception as e:
            return JSONResponse({"msg": str(e)}, 400)

@app.post('/qrcode/get')
def get_qrcode():
    global driver_controller, qr_code
    try:
        qr_code = True
        driver_controller.driver.quit()
        driver_controller = DriverController('https://web.whatsapp.com/', cache=True, hadless=False, remove_data=True)
        qrcode_repository = QrCodeController(driver_controller)
        image_data = qrcode_repository.get_image()
        return Response(content=image_data, media_type="image/png")
    except Exception as e:
        return JSONResponse({"msg": str(e)})

@app.post('/qrcode/confirm')
def confirm_qrcode():
    global driver_controller, qr_code
    qrcode_repository = QrCodeController(driver_controller)
    response = qrcode_repository.check_page()
    if response:
        qr_code = False
        driver_controller.driver.quit()
        driver_controller = DriverController('https://web.whatsapp.com/', cache=True, hadless=True)
        return Response(content="configurado com sucesso!", status_code=200)
    else:
        return Response(content="Aguarde um pouco e tente novamente, ou tente reconectar!", status_code=200)
