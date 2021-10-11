import json
import os
from datetime import datetime

# 형태소 분석
from konlpy.tag import Kkma
from wordcloud import WordCloud


def get_time_str():
    return "[" + str(datetime.now()) + "]"


def get_pos_tag(target_text):
    """ pos tagging
    :param target_text: 입력 텍스트(OCR 결과)
    :return dictionary (pos tagging 결과)"""

    # 1. pos tagger initialization
    print(get_time_str(), "=== step 3 ===")
    print(get_time_str(), "pos tagger initializing....")
    kkma = Kkma()
    kkma.pos("시작")
    print(get_time_str(), "pos tagger initialized...")

    # 2. 대상 텍스트 pos tagging
    print(get_time_str(), "pos tagging 시작...")
    pos_tagged_results = kkma.pos(target_text)
    print(get_time_str(), f"pos tagging 결과를 출력합니다.\n{pos_tagged_results}")
    print(get_time_str(), "pos tagging 완료...")

    return pos_tagged_results


def get_target_word(pos_tagged_results):
    """
    원하는 품사에 해당하는 단어를 뽑아 리스트로 반환한다.
    :param pos_tagged_results:
    :return: list
    """

    word_list = []

    for pos in pos_tagged_results:
        if pos[1][0] in {"I", "M", "N", "O", "U", "V"}:
            word_list.append(pos[0])

    print(get_time_str(), f"{len(pos_tagged_results)}중에 {len(word_list)}개를 추출하였습니다.")

    # 단어의 리스트를 출력한다.
    print(get_time_str(), f"단어의 리스트를 출력합니다. \n{word_list}\n")

    return word_list


def save_list(result_file_name, target_list):
    """
    단어의 리스트를 저장한다. -> 이 단어 리스트로 word cloud를 만들 예정.

    :param result_file_name : 파일 이름
    :param target_list : 저장하고자 하는 list
    :return None
    """

    with open(result_file_name, "w") as list_file:
        list_file.write(target_list)


def make_word_cloud(word_list):
    """
    단어의 list를 받아서 word cloud를 만들고, WordCloud 객체를 반환한다.

    :param word_list: list
    :return: WordCloud object
    """

    # word cloud에 넣기 위해 str형태로 반환
    word_list_str = ",".join(word_list)

    # word cloud 객체 생성
    wc = WordCloud(background_color="white", max_font_size=100,
                   font_path='/Users/motive/Library/Fonts/D2Coding-Ver1.3.2-20180524-all.ttc',
                   max_words=10)

    # word cloud 생성.
    cloud = wc.generate(word_list_str)

    return cloud


def word_relations():
    """ 연관어 분석. 긍정/부정일때 자주 등장한 단어가 무엇인지 분석함.
        1. 긍정/부정 별 문장들을 감성분석 결과에서 가져와야 함.
        2. 가져온 결과에서 sentence들을 붙인다.
        3. sentence들을 pos tagging + 원하는 품사를 뽑는다.

        :return 리스트
        이후에 워드클라우드를 그리면 됨.
        """
    pass


def text_mining(user_id):
    """
    텍스트 분석 main function.
    - pos tagging, 원하는 품사의 단어를 추출
    - word cloud를 그리고, 저장한다.

    :param user_id: str, user의 id
    :var user_ocr_path:
    :var result_file_path:
    :var word_cloud_file_path:
    :return: None
    """

    # 경로 변수 정의
    user_ocr_path = os.path.join(os.path.dirname(__file__), "../results", str(user_id), f"{str(user_id)}_ocr.txt")
    result_file_path = os.path.join(os.path.dirname(__file__), "../results", str(user_id), user_id + "_" + "word_list.txt")
    word_cloud_file_path = os.path.join(os.path.dirname(__file__), '../results', str(user_id), user_id + "_" + "word_cloud.png")

    # --- 분석한 리스트가 있으면 그걸 가져옴
    if os.path.isfile(result_file_path):
        # 워드클라우드 만들기
        with open(result_file_path, "r") as word_list:
            cloud = make_word_cloud(word_list)
            # 저장하기
            cloud.to_file(word_cloud_file_path)


    # --- 분석한 리스트가 없으면 pos tagging을 실시함.
    else:
        # 1. POS tagging 한다.
        # 원래는 OCR 결과로 텍스트 분석을 해야하는데 일단은 샘플 텍스트로 실시한다.
        with open(user_ocr_path, "r") as target_text:
            print(type(target_text))
            pos_tag_results = get_pos_tag(target_text.read())

        # 2. 특정 품사를 가진 단어만 뽑아 list로 만든다.
        word_list = get_target_word(pos_tag_results)

        # 2-1. 단어 list를 파일로 저장한다.
        save_list(result_file_path, word_list)

        # 3. 워드 클라우드를 만든다
        cloud = make_word_cloud(word_list)

        # 3-1 워드클라우드를 저장한다.
        cloud.to_file(word_cloud_file_path)

    print(get_time_str(), "종료합니다...")

