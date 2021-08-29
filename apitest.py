import io
import os
from datetime import datetime
import json

# Imports the Google Cloud client library
from google.cloud import vision
from hanspell import spell_checker

# 형태소 분석
from konlpy.tag import Kkma, Komoran

# word cloud 그리기
import matplotlib.pyplot as plt
from wordcloud import WordCloud



def getTimeStr():
    return "[" + str(datetime.now()) + "]"


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


def get_pos_tag(text):
    """ pos tagging -> 원하는 품사에 해당하는 단어만 뽑아내기 """

    # 1. pos tagger initialization
    print(getTimeStr(), "=== step 3 ===")
    print(getTimeStr(), "pos tagger initializing....")
    kkma = Kkma()
    kkma.pos("시작")
    print(getTimeStr(), "pos tagger initialized...")

    # 2. 대상 텍스트 pos tagging
    print(getTimeStr(), "pos tagging 시작...")
    pos_tagged_results = kkma.pos(text)
    print(f"pos tagging 결과를 출력합니다.\n{pos_tagged_results}")
    print(getTimeStr(), "pos tagging 완료...")

    return pos_tagged_results


def get_target_word(pos_tagged_results):
    # 2. 원하는 품사에 해당하는 단어만 뽑아내기
    word_list = []

    for pos in pos_tagged_results:
        if pos[1][0] in {"I", "M", "N", "O", "U", "V"}:
            word_list.append(pos[0])

    print(getTimeStr(), f"{len(pos_tagged_results)}중에 {len(word_list)}개를 추출하였습니다.")


    # 단어의 빈도를 출력한다.
    word_frequency = get_frequency(word_list)
    print(getTimeStr(), f"단어의 빈도는 \n{word_frequency}\n")

    # 빈도 결과를 저장한다.


    # 단어의 리스트를 출력한다.
    print(getTimeStr(), f"단어의 리스트를 출력합니다\n{word_list}\n")

    return word_list

def get_frequency(word_list):
    """ list에 있는 단어들의 빈도를 {단어:빈도}의 딕셔너리 형태로 반환한다. """
    print(getTimeStr(), "단어의 빈도를 확인합니다.")
    word_freq_dict = {}
    for word in word_list:  # 리스트에 있는 단어를 하나씩 조회함.
        if word in word_freq_dict:  # dict에 한개라도 있으면 개수를 올림
            word_freq_dict[word] += 1
        elif word not in word_freq_dict:  # 한개도 없으면 그 단어 key에 대한 값은 1이 된다.
            word_freq_dict[word] = 1
    print(getTimeStr(), "단어의 빈도 확인 완료, 딕셔너리를 반환")

    return word_freq_dict



def save_result(resultFileName, word_freq):
    with open(resultFileName, "w") as json_file:
        json.dump(word_freq, json_file, ensure_ascii=False)

def save_list(result_file_name, target_list):
    # 단어의 리스트를 저장한다.
    with open(result_file_name, "w") as list_file:
        list_file.write(f"{target_list}")


# 3. 위 결과를 감성 분석 API로 보낸다.

# 4. 텍스트 마이닝 - 빈발단어 워드 클라우드..
# 1) 한글 형태소 분석, konlpy ->
# 2) 불용어 처리 - 조사 어미 등 제외
# 3) 구문분석 -
# 4) 분석대상 선정 / 분석


def make_word_cloud(word_list):
    """ 단어의 list를 받아서 word cloud를 만들고, 출력한다."""

    # word cloud에 넣기 위해 str형태로 반환
    word_list_str = ",".join(word_list)

    # word cloud를 만든다.
    wc = WordCloud(background_color="white", max_font_size=100,
                   font_path='/Users/motive/Library/Fonts/D2Coding-Ver1.3.2-20180524-all.ttc',
                   max_words=10)

    cloud = wc.generate(word_list_str)

    # word cloud를 출력한다.
    print(getTimeStr(), "Word Cloud를 출력합니다.")
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()

""" OCR -> spell check -> 저장
    
    -> pos tagging -> target word -> 저장
    """
def text_mining():
    user_id = 'donkey'  # 나중에 flask에서 객체화된 id를 받을 것.
    result_file_name = "./results/" + user_id + "_" + "word_list.txt"

    if os.path.isfile(result_file_name):  # 분석한 리스트가 있으면 그걸 가져옴
        with open(result_file_name, "r") as word_list:
            make_word_cloud(word_list)

    else:  # 분석한 리스트가 없으면 pos tagging을 실시함.
        with open("sampletext.txt", "r") as sample_text:
            print(type(sample_text))
            pos_tag_results = get_pos_tag(sample_text.read())

        word_list = get_target_word(pos_tag_results)
        save_list(result_file_name, word_list)
        make_word_cloud(word_list)
    print(getTimeStr(), "종료합니다...")


if __name__ == "__main__":
    # text = OCRrequest2()
    # spell_check(text)

    text_mining()
