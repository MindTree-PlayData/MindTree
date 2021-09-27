import io
import os
from datetime import datetime

from hanspell import spell_checker

# Imports the Google Cloud client library
from google.cloud import vision


def get_time_str():
    return "[" + str(datetime.now()) + "]"


def spell_check(input_text):
    result = spell_checker.check(input_text)
    print(type(result))
    print(get_time_str(), "\n\noriginal")
    print(result.original)
    print(get_time_str(), "\n\nchecked")
    print(result.checked)
    print(get_time_str(), "\n\nwords")
    print(result.words)


def request_ocr(content):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)

    # 이미지에서 text를 추출한다.
    response_text = client.text_detection(image=image)
    words = response_text.text_annotations

    # 첫번째 결과를 줄바꿈 없이 모두 붙여서 출력한다. #
    # words[0]는 추출된 모든 텍스트를 모은 정보인데, 그 중 decription이라는 key에 저장된 값이 인식된 텍스트의 문자열이다.
    # 줄바꿈이 있으므로 제외하고 모아준다.
    print("------------아래는 뽑은 텍스트 입니다---------------")

    # words_cat = words[0].description.replace("\n", "")
    words_cat = words[0].description  # 줄바꿈 없이 해봤음
    print(f'뽑힌 텍스트 \n{words[0].description}')
    # print("\n\n이건 replace한 텍스트\n", words_cat)

    return words_cat


def ocr(filepath, user_id):
    # Loads the image into memory
    with io.open(filepath, 'rb') as image_file:
        content = image_file.read()
    text = request_ocr(content)
    spell_check(text)

    # 결과 저장하기
    user_path = os.path.join("./results", str(user_id))
    user_ocr_path = os.path.join(user_path, f"{str(user_id)}_ocr.txt")
    # print(user_path)
    # print(user_ocr_path)

    if not os.path.isdir(user_path):
        os.makedirs(user_path, exist_ok=True)  # 없으면 만들고 있으면 지나감

    with open(user_ocr_path, "w") as ocr_result:
        ocr_result.write(text)

    return text
