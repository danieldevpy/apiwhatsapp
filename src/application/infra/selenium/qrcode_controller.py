from src.application.repository.qrcode_repository import QrCodeRepository
from src.application.infra.selenium import elements
import base64


class QrCodeController(QrCodeRepository):


    def get_image(self):
        qrcode_element = self.controller.get_element(elements.qrcode_image)
        image_base64 = self.controller.driver.execute_script("""
            var canvas = arguments[0];
            return canvas.toDataURL('image/png').substring(22); // remove 'data:image/png;base64,' prefix
        """, qrcode_element)
        image_data = base64.b64decode(image_base64)
        return image_data
    
    def check_page(self):
        try:
            self.controller.get_element(elements.page_wpp)
            return True
        except:
            return False