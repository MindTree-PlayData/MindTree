import io
import os
from datetime import datetime
from konlpy.tag import Komoran
# Imports the Google Cloud client library
from google.cloud import vision
from hanspell import spell_checker

def OCRrequest():
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/data5.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    response_text = client.text_detection(image=image)
    words = response_text.text_annotations

    print("------------아래는 분석한 Label입니다.---------------")
    for label in labels:
        print(label.description)

    print("------------아래는 뽑은 텍스트 입니다---------------")
    for word in words:
        print(word.description)


def OCRrequest2(useapi):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources/pc_img.png')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

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

    # komoran = Komoran()
    # komoran.pos(words_cat)


def spell_check(input_text):
    result = spell_checker.check(input_text)
    print(type(result))
    print("\n\noriginal")
    print(result.original)
    print("\n\nchecked")
    print(result.checked)
    print("\n\nwords")
    print(result.words)


# 1. 모든 결과를 한 줄로 붙인다.

# 2. nlp 라이브러리 등을 이용해서 보정한다.
# 띄어쓰기, 문장 분리 등 처리를 한다.

# 3. 위 결과를 감성 분석 API로 보낸다.



# 4. 텍스트 마이닝 - 빈발단어 워드 클라우드..
    # 1) 한글 형태소 분석, konlpy
    # 2) 불용어 처리 - 조사 어미 등 제외
    # 3) 구문분석 -
    # 4) 분석대상 선정 / 분석


if __name__ == "__main__":
    text = OCRrequest2()
    spell_check(text)
