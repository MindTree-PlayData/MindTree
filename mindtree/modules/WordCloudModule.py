from wordcloud import WordCloud

from mindtree import db
from mindtree.models import Post
from mindtree.utils.VO import VO
from util import get_time_str


class WCModule(VO):

    def __init__(self):
        super().__init__()

        # WordCloud 객체 initialization
        self.wc = WordCloud(background_color="white", max_font_size=100,
                            max_words=10)

        self.word_list: str = ''
        self.cloud: object = None

        print(get_time_str(), "Word Cloud 생성 객체 초기화 완료")

    def make_word_cloud(self, word_list, post_id):
        """ 단어의 list를 받아서 word cloud를 만들고, WordCloud 객체를 반환한다. """
        self.set_user_word_cloud_object(word_list)
        self.save_word_cloud(post_id)

    def set_user_word_cloud_object(self, word_list: list):

        # word cloud에 넣기 위해 str형태로 반환
        if word_list:
            _word_list_str: str = ",".join(word_list)
        else:
            _word_list_str = ",".join(self.word_list)

        # word cloud 생성.
        self.cloud = self.wc.generate(_word_list_str)

    def save_word_cloud(self, post_id):
        # 로컬에 파일로 저장
        self.cloud.to_file(super().get_user_word_cloud_path(post_id))

        # 워드 클라우드 이미지 파일명을 DB에 저장한다.
        post = Post.query.get_or_404(post_id)
        post.word_cloud = super().get_user_word_cloud_file_name(post_id)
        db.session.commit()
        print(get_time_str(), "TextAnalysis: word cloud 저장 완료")

