from wordcloud import WordCloud
import os
from mindtree import db
from mindtree.models import Post
from mindtree.utils.DTO import PathDTO
from mindtree.modules.util import get_time_str


class CreateWordCloud(PathDTO):

    def __init__(self):
        super().__init__()

        # WordCloud 객체 initialization
        self.wc = WordCloud(font_path='fonts/NanumSquareRoundB.ttf',
                            background_color="white", max_font_size=100, max_words=10)
        print("[CreateWordCloud] os.getcwd(): ", os.getcwd())
        self.word_list: str = ''
        self.cloud: object = None

        print(get_time_str(), "Word Cloud 생성 객체 초기화 완료")

    def make_word_cloud(self, word_list, post_id):
        """ 단어의 list를 받아서 word cloud를 만들고, WordCloud 객체반환 """
        self._set_user_word_cloud_object(word_list)
        self._save_word_cloud(post_id)

    def _set_user_word_cloud_object(self, word_list: list):

        # word cloud에 넣기 위해 str형태로 반환
        if word_list:
            _word_list_str: str = ",".join(word_list)
        else:
            print("word_list가 없습니다.")
            _word_list_str = ",".join(self.word_list)

        # word cloud 생성
        self.cloud = self.wc.generate(_word_list_str)

    def _save_word_cloud(self, post_id):
        # 로컬에 파일로 저장
        self.cloud.to_file(super().get_user_word_cloud_path(post_id))

        # 워드 클라우드 이미지 파일명을 DB에 저장
        if post_id:
            print("[_save_word_cloud] post_id: ", post_id)
            post = Post.query.get_or_404(post_id)
            post.word_cloud = super().get_user_word_cloud_file_name(post_id)
            db.session.commit()
            print(get_time_str(), "TextAnalysis: word cloud 저장 완료")
        else:
            print("게시물을 찾을 수 없습니다.")

