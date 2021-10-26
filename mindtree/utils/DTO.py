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
        print("_username: ", self._username)  # 유닛테스트용.
        return os.path.join(self._user_media_path, f"{self._username}_{str(post_id)}_word_cloud.png")

    def get_user_word_cloud_file_name(self, post_id: int):
        self._set_user_variables(post_id)  # self._username 을 설정하는 용도.
        return f"{self._username}_{str(post_id)}_word_cloud.png"


    # # 기능: DB에서 유저 정보를 조회해 upload 이미지 파일 이름을 반환하는 용도.
    # # 입력: Post 테이블에서 user_id를, User 테이블에서 username을 조회해서 입력
    # # 출력: {username}_{post_id}.png라는 이름의 업로드 이미지 파일 이름을 반환
    # # 개발자: 김수연
    # # 버전/일시: ver 0.x/2021.10.26
    # def get_user_upload_img_file_name(self, post_id: int):
    #     '''
    #     Post 테이블에서 user_id를, User 테이블에서 username을 조회해 upload 이미지 파일 이름 반환
    #     '''
    #     self._set_user_variables(post_id)  
    #     return f"{self._username}_{str(post_id)}.png"


    def get_user_sentiment_path(self, post_id: int):
        self._set_user_variables(post_id)
        self._set_user_media_path()
        return os.path.join(self._user_media_path, f"{str(self._username)}_{str(post_id)}_sentiment.json")


if __name__ == '__main__':
    """ 유닛 테스트 방법:
    MindTree (루트경로에서) 
    $ python mindtree/utils/DTO.py  """
    vo = PathDTO()
    print(vo.get_user_word_cloud_path(2))  # post_id가 2인 word cloud 저장 경로를 가져온다.
