import os
from .util import get_time_str
from mindtree import USER_BASE_PATH, db
from mindtree.models import Post

# 형태소 분석
from konlpy.tag import Kkma
from wordcloud import WordCloud

class TextAnalysis:

    def __init__(self):
        # pos tagger initialization
        print(get_time_str(), "TextAnalysis: pos tagger initializing....")
        self.kkma = Kkma()
        self.kkma.pos("시작")
        print(get_time_str(), "TextAnalysis: pos tagger initialized...")

        # WordCloud 객체 initialization
        self.wc = WordCloud(background_color="white", max_font_size=100,
                            font_path='/Users/motive/Library/Fonts/D2Coding-Ver1.3.2-20180524-all.ttc',
                            max_words=10)

        # 빈 경로 변수 설정
        self.ocr_text_path = ''
        self.word_list_file_path = ''
        self.word_cloud_file_path = ''

        # 빈 결과 변수 설정
        self.pos_tagged_results: dict = {}
        self.word_list: list = []

        print(get_time_str(), "TextAnalysis: initialized...")

    def init_user_path(self, user_id: str, post_id) -> None:
        """ 유저 id를 받아 경로 변수를 설정한다. """
        self.word_cloud_file_path = os.path.join(USER_BASE_PATH, str(user_id), f"{user_id}_{str(post_id)}" +
                                                 "_word_cloud.png")
        self.word_list_file_path = os.path.join(USER_BASE_PATH, str(user_id), f"{user_id}_{str(post_id)}" +
                                                "_word_list.txt")
        self.ocr_text_path = os.path.join(USER_BASE_PATH, str(user_id), f"{user_id}_{str(post_id)}_ocr.txt")

    def get_pos_tag(self, target_text: str) -> dict:
        """ pos tagging
        :param target_text: 입력 텍스트(OCR 결과)
        :return pos tagging 결과 """

        print(get_time_str(), "TextAnalysis: pos tagging 시작...")
        self.pos_tagged_results = self.kkma.pos(target_text)
        # print(get_time_str(), f"pos tagging 결과를 출력합니다.\n{self.pos_tagged_results}")
        print(get_time_str(), "TextAnalysis: pos tagging 완료...")

        return self.pos_tagged_results

    def get_target_words(self) -> list:
        """
        원하는 품사에 해당하는 단어를 뽑아 리스트로 반환한다.
        """
        for pos in self.pos_tagged_results:
            if pos[1][0] in {"N", "V"}:
                self.word_list.append(pos[0])
        print(get_time_str(), f"TextAnalysis: {len(self.pos_tagged_results)}중에 {len(self.word_list)}개를 추출하였습니다.")
        # print(get_time_str(), f"단어의 리스트를 출력합니다. \n{self.word_list}\n")

        return self.word_list

    def save_list(self):
        """
        단어의 리스트를 저장한다. -> 이 단어 리스트로 word cloud를 만들 예정.
        """
        # 리스트는 write() 할 수 없어서 str으로 만듬.
        _word_list_str = ",".join(self.word_list)

        with open(self.word_list_file_path, "w") as list_file:
            list_file.write(_word_list_str)
            print(get_time_str(), "TextAnalysis: 단어 리스트 저장 완료")

    def make_word_cloud(self, word_list=None) -> object:
        """
        단어의 list를 받아서 word cloud를 만들고, WordCloud 객체를 반환한다.
        :return: WordCloud object
        """
        # word cloud에 넣기 위해 str형태로 반환
        if word_list:
            _word_list_str: str = ",".join(word_list)
        else:
            _word_list_str = ",".join(self.word_list)

        # word cloud 생성
        cloud = self.wc.generate(_word_list_str)
        return cloud

    def text_mining(self, user_id: str, post_id: int) -> None:
        """
        텍스트 분석 main function.
        - pos tagging, 원하는 품사의 단어를 추출
        - word cloud를 그리고, 저장한다.
        """
        # 사용자 정보를 이용하여 경로변수를 설정한다.
        self.init_user_path(user_id, post_id)

        # --- 분석한 리스트가 있으면 그걸 가져옴
        if os.path.isfile(self.word_list_file_path):
            # 워드클라우드 만들기
            with open(self.word_list_file_path, "r") as word_list:
                print(type(word_list))
                cloud = self.make_word_cloud(word_list)
                # 저장하기
                cloud.to_file(self.word_cloud_file_path)
                post = Post.query.get_or_404(post_id)
                post.word_cloud = f"{user_id}_{str(post_id)}_word_cloud.png"
                db.session.commit()
                print(get_time_str(), "TextAnalysis: word cloud 저장 완료")

        # --- 분석한 리스트가 없으면 pos tagging을 실시함.
        else:
            # 1. POS tagging 한다.
            # ocr text db에서 가져오기
            ocr_text = Post.query.get(post_id).ocr_text
            self.pos_tagged_results = self.get_pos_tag(ocr_text)

            # 2. 특정 품사를 가진 단어만 뽑아 list로 만든다.
            self.get_target_words()

            # 2-1. 단어 list를 파일로 저장한다.
            self.save_list()

            # 3. 워드 클라우드를 만든다
            cloud = self.make_word_cloud()

            # 3-1 워드클라우드를 저장한다.
            cloud.to_file(self.word_cloud_file_path)

            # 3-2 워드 클라우드 이미지 파일명을 DB에 저장한다.
            # post_id가 있으면 알수 있는 형식이기 때문에 삭제 또는 다른방식을 대체 예정
            post = Post.query.get_or_404(post_id)
            post.word_cloud = f"{user_id}_{str(post_id)}_word_cloud.png"
            db.session.commit()
            print(get_time_str(), "TextAnalysis: word cloud 저장 완료")

        print(get_time_str(), "Text Analysis 완료...")
