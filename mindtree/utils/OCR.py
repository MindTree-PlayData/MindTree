import io
import os
from utils import get_time_str

from hanspell import spell_checker

# Imports the Google Cloud client library
from google.cloud import vision

USER_BASE_PATH = '/Users/motive/Data_Study/Projects/MindTree/mindtree/results/'


class OCR:

    def __init__(self):
        # GOOGLE VISION API 객체 initiation
        self.client = vision.ImageAnnotatorClient()

        # 빈 경로 변수 설정
        self.image_path = ''
        self.save_path = ''

        # 빈 text 변수 설정
        self.ocr_text: str = ''
        self.ocr_text_spell_checked: str = ''

    def init_user_path(self, user_id):
        self.image_path = os.path.join(USER_BASE_PATH, user_id, user_id + "_pc_img.png")
        self.save_path = os.path.join(USER_BASE_PATH, user_id, user_id + "_ocr.txt")

    def ocr_request(self, image_content: bytes):
        _image = vision.Image(content=image_content)
        _ocr_response = self.client.text_detection(image=_image)
        text_annotations = _ocr_response.text_annotations

        self.ocr_text = text_annotations[0].description
        return self.ocr_text

    def spell_check(self, input_text):
        self.ocr_text_spell_checked = spell_checker.check(input_text).checked

        return self.ocr_text_spell_checked

    def save_file(self):
        """ OCR 결과를 저장한다."""
        with open(self.save_path, "w") as ocr_result:
            ocr_result.write(self.ocr_text_spell_checked)

    def ocr_main(self, user_id: str):
        """ ocr 실행 메인 함수 """
        self.set_user_path(user_id=user_id)
        with io.open(self.image_path, 'rb') as image_file:
            image_content = image_file.read()
            print(type(image_content))
        self.ocr_request(image_content)
        self.spell_check(self.ocr_text)
        self.save_file()


user_id = 'toptoptop'
ocr = OCR()
ocr.ocr_main(user_id)