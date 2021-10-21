import os
from mindtree.modules.util import get_time_str
from mindtree.models import Post
from mindtree.modules.WordCloudModule import WCModule

# 형태소 분석
from konlpy.tag import Kkma


class TextAnalysis(WCModule):

    def __init__(self):
        """ WCModule에서 WordCloud 객체와, DTO를 이 클래스에서 사용한다. """
        super().__init__()

        # pos tagger initialization
        print(get_time_str(), "TextAnalysis: pos tagger initializing....")
        self.kkma = Kkma()
        self.kkma.pos("시작")

        # 빈 경로 변수 설정
        #   __init__ 에 post_id를 넣어 바로 정할 수도 있지만,
        #   Kkma()를 로드하는 절차와 분리하기 위해서 이후에 설정한다.
        self.ocr_text_path = ''
        self.word_list_file_path = ''

        # 빈 결과 변수 설정
        self.ocr_text: str = ''
        self._pos_tagged_results: dict = {}
        self.word_list: list = []

        print(get_time_str(), "TextAnalysis: initialized...")

    def text_analysis(self, post_id: int):
        """ 텍스트 분석 main function.
        - pos tagging, 원하는 품사의 단어를 추출
        - word cloud를 그리고, 저장한다. """

        # Post_id 정보를 이용하여 경로변수를 설정한다.
        self.word_list_file_path = super().get_user_word_list_path(post_id)
        self.ocr_text_path = super().get_user_ocr_file_path(post_id)

        # --- 분석한 리스트가 있으면 그걸로 워드클라우드를 만든다.
        if os.path.isfile(self.word_list_file_path):
            # 워드클라우드 만들기
            with open(self.word_list_file_path, "r") as word_list:
                print(type(word_list))

                # 로컬에 워드클라우드 파일 저장, DB에 워드클라우드 파일 이름 저장.
                super().make_word_cloud(word_list, post_id)

        # --- 분석한 리스트가 없으면 pos tagging을 실시함.
        else:
            # 1. POS tagging 한다.
            # ocr text db에서 가져오기
            self.ocr_text = Post.query.get(post_id).ocr_text
            self._get_pos_tag()

            # 2. 특정 품사를 가진 단어만 뽑아 list로 만든다.
            self._get_target_words()

            # 2-1. 단어 list를 파일로 저장한다.
            self._save_list()

            # 3. 워드 클라우드를 만들어 저장한다.
            super().make_word_cloud(self.word_list, post_id)

        print(get_time_str(), "Text Analysis 완료...")

    def _get_pos_tag(self):
        print(get_time_str(), "TextAnalysis: pos tagging 시작...")

        self._pos_tagged_results = self.kkma.pos(self.ocr_text)

        print(get_time_str(), "TextAnalysis: pos tagging 완료...")

    def _get_target_words(self):
        """ 원하는 품사에 해당하는 단어를 뽑아 리스트로 반환한다. """
        for pos in self._pos_tagged_results:
            if pos[1][0] in {"N", "V"}:
                self.word_list.append(pos[0])

        print(get_time_str(), f"TextAnalysis: {len(self._pos_tagged_results)}중에 {len(self.word_list)}개를 추출하였습니다.")

    def _save_list(self):
        """ 단어의 리스트를 저장한다. -> 이 단어 리스트로 word cloud를 만들 예정. """

        # 리스트는 write() 할 수 없어서 str으로 만듬.
        _word_list_str = ",".join(self.word_list)

        with open(self.word_list_file_path, "w") as list_file:
            list_file.write(_word_list_str)
            print(get_time_str(), "TextAnalysis: 단어 리스트 저장 완료")


# 동기 로컬 폰트
# font_path='/Users/motive/Library/Fonts/D2Coding-Ver1.3.2-20180524-all.ttc',

if __name__ == '__main__':
    ta = TextAnalysis()
    ta.text_analysis(2)
