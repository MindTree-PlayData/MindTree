import os
from mindtree.utils.util import get_time_str
from mindtree.models import Post
from mindtree.modules.word_cloud import CreateWordCloud
from soylemma import Lemmatizer

# 형태소 분석
from konlpy.tag import Kkma


class TextAnalysis(CreateWordCloud):

    def __init__(self):
        """ CreateWordCloud에서 WordCloud 객체와, DTO를 이 클래스에서 사용한다. """
        super().__init__()

        # pos tagger initialization
        print(get_time_str(), "TextAnalysis: pos tagger initializing....")
        self.kkma = Kkma()
        self.kkma.pos("시작")

        # lemmatizer initialization
        self.lemmatizer = Lemmatizer()

        # 빈 경로 변수 설정
        #   __init__ 에 post_id를 넣어 바로 정할 수도 있지만,
        #   Kkma()를 로드하는 절차와 분리하기 위해서 이후에 설정한다.
        self.ocr_text_path = ''
        self.word_list_file_path = ''

        # 빈 결과 변수 설정
        self.ocr_text = ''
        self._pos_tagged_results = {}
        self.word_list = []

        print(get_time_str(), "TextAnalysis: initialized...")

    def text_analysis(self, post_id):
        """ 텍스트 분석 main function.
        - pos tagging, 원하는 품사의 단어를 추출
        - word cloud를 그리고, 저장한다. """

        # Post_id 정보를 이용하여 경로변수를 설정한다.
        print("[text_analysis] post_id: ", post_id)
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
            try:
                self._save_list()

                # 3. 워드 클라우드를 만들어 저장한다.
                super().make_word_cloud(self.word_list, post_id)

            except Exception as e:
                print("[text_analysis]: 단어 list 저장 실패", e)

        print(get_time_str(), "Text Analysis 완료...")

    def _get_pos_tag(self):
        print(get_time_str(), "TextAnalysis: pos tagging 시작...")

        self._pos_tagged_results = self.kkma.pos(self.ocr_text)

        print(get_time_str(), "TextAnalysis: pos tagging 완료...")

    def _get_target_words(self):
        """ 원하는 품사에 해당하는 단어를 뽑아 리스트로 반환한다. """
        print("self._pos_tagged_results: \n", self._pos_tagged_results)
        # 명사
        for pos in self._pos_tagged_results:
            if pos[1] in ["NNG", "NNP"]:
                self.word_list.append(pos[0])

        # 용언(동사, 형용사)
        for i, pos in enumerate(self._pos_tagged_results):
            if pos[1] in ["VV", "VA"]:
                j = 1
                eomi_temp = []
                while self._pos_tagged_results[i+j][1][0] == "E":  # 어간에 붙은 어미를 모두 하나로 만듬
                    eomi_temp.append(self._pos_tagged_results[i+j][0])
                    j += 1
                eomis = "".join(eomi_temp)

                # 어간과 어미를 합친 형태를 만든다. (conjugate)
                # -> 어미가 여러개라도 conjugate함수 자체가 어미 하나의 str을 받게 되어 있어서 붙여서 줘야한다.
                _conjugated = self.lemmatizer.conjugate(pos[0], eomis)[0]
                # print("_conjugated: ", _conjugated)
                try:
                    # 용언의 활용형(conjugate된 단어)에서 기본형을 추출한다.
                    _lemmatized = self.lemmatizer.lemmatize(_conjugated)[0][0]
                    self.word_list.append(_lemmatized)
                except Exception as e:
                    print(f"lemmatization error: {e}\n\t->오류 발생 어간: {pos[0]}")

        print("[_get_target_words] self.word_list: \n", self.word_list)

        print(get_time_str(), f"TextAnalysis: {len(self._pos_tagged_results)}중에 {len(self.word_list)}개를 추출하였습니다.")

    def _save_list(self):
        """ 단어의 리스트를 저장한다. -> 이 단어 리스트로 word cloud를 만들 예정. """

        # 리스트는 write() 할 수 없어서 str으로 만듬.
        _word_list_str = ",".join(self.word_list)

        with open(self.word_list_file_path, "w") as list_file:
            list_file.write(_word_list_str)
            print(get_time_str(), "TextAnalysis: 단어 리스트 저장 완료")

        return True


if __name__ == '__main__':
    """ 유닛 테스트 방법:
        MindTree (루트경로에서) 
        $ python mindtree/modules/text_analysis.py  """
    ta = TextAnalysis()
    ta.text_analysis(2)
    # lm = Lemmatizer()
    # a = lm.lemmatize("말하여")
    # print(a)
