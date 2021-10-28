import os
from mindtree.config import PathConfig
from mindtree.models import Post, User


class PathDTO(PathConfig):

    def __init__(self):
        self.DIARY_FILE_PATH = ''
        self.WORD_CLOUD_FILE_PATH = ''
        self._user_id = ''
        self._username = ''
        self._user_media_path = ''

    def _set_user_variables(self, post_id: int):
        """ 경로를 찾는 메서드에서 쓰기 위한 유저 정보를 변수에 저장한다. """
        self._user_id = Post.query.get(post_id).user_id  # post_id를 받아 Post의 user_id를 조회한다.
        self._username = User.query.get(self._user_id).username  # user_id를 받아 User의 username을 조회한다.

    def _set_user_media_path(self):
        """ MEDIA_PATH 에 회원의 경로를 설정한다.
        - self._set_user_variables 이후에 호출되어야 한다.
        - 예를 들어 self._username 이 donkey라면,
            /Users/motive/Data_Study/Projects/MindTree/mindtree/results/ 를 설정한다."""
        self._user_media_path = os.path.join(self.MEDIA_PATH, self._username)

    ###############################################################################
    # Callable Methods ############################################################

    def get_user_diary_file_name(self, post_id):
        self._set_user_variables(post_id)
        self._set_user_media_path()
        return f"{self._username}_{str(post_id)}.png"

    def get_user_media_path(self, post_id):
        self._set_user_variables(post_id)
        self._set_user_media_path()
        return self._user_media_path

    def get_user_diary_file_path(self, post_id: int):
        self._set_user_variables(post_id)
        self._set_user_media_path()
        return os.path.join(self._user_media_path, f"{self._username}_{str(post_id)}.png")

    def get_user_ocr_file_path(self, post_id: int):
        self._set_user_variables(post_id)
        self._set_user_media_path()

        return os.path.join(self._user_media_path, f"{self._username}_{str(post_id)}_ocr.txt")

    def get_user_word_list_path(self, post_id: int):
        self._set_user_variables(post_id)
        self._set_user_media_path()

        return os.path.join(self._user_media_path, f"{self._username}_{str(post_id)}_word_list.txt")

    def get_user_word_cloud_path(self, post_id: int):
        self._set_user_variables(post_id)
        self._set_user_media_path()
        # print("[get_user_word_cloud_path] _username: ", self._username)  # 유닛테스트용.
        return os.path.join(self._user_media_path, f"{self._username}_{str(post_id)}_word_cloud.png")

    def get_user_word_cloud_file_name(self, post_id: int):
        self._set_user_variables(post_id)  # self._username 을 설정하는 용도.
        return f"{self._username}_{str(post_id)}_word_cloud.png"

    def get_user_sentiment_path(self, post_id: int):
        self._set_user_variables(post_id)
        self._set_user_media_path()
        return os.path.join(self._user_media_path, f"{str(self._username)}_{str(post_id)}_sentiment.json")


    # 기능: 스택 바 차트 파일 이름을 반환하는 함수
    # 입력: 유저 정보를 input
    # 출력: 스택 바 차트 파일 이름을 output
    # 개발자: 김수연
    # 버전/일시: 0.x/2021.10.28
    def get_user_stacked_bar_chart_file_name(self, post_id):
        self._set_user_variables(post_id)
        return f"{self._username}_{str(post_id)}_stacked_bar_char.png"
        pass

if __name__ == '__main__':
    """ 유닛 테스트 방법:
    MindTree (루트경로에서) 
    $ python mindtree/utils/DTO.py  """
    vo = PathDTO()
    print(vo.get_user_word_cloud_path(2))  # post_id가 2인 word cloud 저장 경로를 가져온다.
