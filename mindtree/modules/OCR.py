import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from hanspell import spell_checker

from flask_login import current_user
from mindtree import db
from mindtree.utils.VO import VO
from mindtree.models import Post
from util import get_time_str


class OCR(VO):

    # 빈 경로 변수 설정
    image_path: str = ''
    save_path: str = ''

    # 빈 post_id를 설정.
    post_id: int = None

    # 빈 text 변수 설정
    ocr_text: str = ''
    ocr_text_spell_checked: str = ''

    image_content: bytes = ''

    def __init__(self):
        super().__init__()

        # GOOGLE VISION API 객체 initiation
        self.client = vision.ImageAnnotatorClient()
        print(get_time_str(), "OCR initialized....")

    def ocr_request(self):
        _image = vision.Image(content=self.image_content)
        _ocr_response = self.client.text_detection(image=_image)
        text_annotations = _ocr_response.text_annotations

        self.ocr_text = text_annotations[0].description

    def spell_check(self):
        self.ocr_text_spell_checked = spell_checker.check(self.ocr_text).checked

    def save_file(self):
        """ OCR 결과를 저장한다."""
        with open(self.save_path, "w") as ocr_result:
            ocr_result.write(self.ocr_text_spell_checked)

        # DB에 OCR 결과 텍스트를 저장한다.
        post = Post.query.get_or_404(self.post_id)
        post.ocr_text = self.ocr_text_spell_checked
        db.session.commit()

    def ocr_main(self, post_id: int):
        """ ocr 실행 메인 함수 """
        print("OCR.ocr_main", post_id)
        # post_id를 설정한다.
        # OCR 객체가 Post 에 대한 쿼리를 할 때 사용된다.
        self.post_id = post_id

        # 유저의 경로 변수를 저장한다.
        self.image_path = super().get_user_diary_file_path(post_id)
        self.save_path = super().get_user_ocr_file_path(post_id)

        # 이미지 파일을 가져온다.
        with io.open(self.image_path, 'rb') as image_file:
            self.image_content = image_file.read()
            print(type(self.image_content))

        # GOOGLE VISION API 사용하여 OCR 실시.
        self.ocr_request()

        # 스펠링 체크
        self.spell_check()

        # 저장
        self.save_file()

        print(get_time_str(), "OCR 완료")


if __name__ == '__main__':
    """  
    $ python mindtree/modules/OCR.py """
    ocr = OCR()
    ocr.ocr_main(2)
