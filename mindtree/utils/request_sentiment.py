import json
import os

import requests

from mindtree import APP_PATH, USER_BASE_PATH, db
from mindtree.models import Post
from .util import get_time_str

key_path = os.path.join(APP_PATH, "../key/keys.json")
with open(key_path, "r") as keys:
    n_key = json.load(keys)


class SentimentAnalysis:
    # Naver sentiment API 요청 정보
    url = 'https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze'

    headers = {'X-NCP-APIGW-API-KEY-ID': n_key["NAVER_API_KEY_ID"],
               'X-NCP-APIGW-API-KEY': n_key["NAVER_API_KEY"],
               'Content-Type': 'application/json; charset=utf-8'
               }

    def __init__(self):
        # 빈 경로 변수 설정
        self.text_path = ''
        self.sentiment_path = ''

        # ocr 텍스트 파일
        self.ocr_text_data = ''

        self.res = ''  # post 요청 후 반응 객체
        self.json_response = ''  # response 객체의 json 데이터
        print(get_time_str(), "SentimentAnalysis initialized...")

    def init_user_path(self, user_id, post_id) -> None:
        self.text_path = os.path.join(USER_BASE_PATH, str(user_id), f"{str(user_id)}_{str(post_id)}_ocr.txt")
        self.sentiment_path = os.path.join(USER_BASE_PATH, str(user_id), f"{str(user_id)}_{str(post_id)}_sentiment.json")

    def request(self):
        self.res = requests.post(url=self.url,
                                 headers=self.headers,
                                 json={"content": self.ocr_text_data}
                                 )
        self.json_response = self.res.json()

        if self.res.status_code == 200:
            return self.json_response
        else:
            print(f"{get_time_str()} SentimentAnalysis: request error! {self.res.status_code}")
            return None

    def save_response(self, post_id: int) -> None:
        with open(self.sentiment_path, "w", encoding='utf-8') as f:
            json.dump(self.json_response, f, indent='\t', ensure_ascii=False)
            print(get_time_str(), "SentimentAnalysis: 감성분석 저장 완료")

        post = Post.query.get_or_404(post_id)
        post.sentiment = self.json_response
        db.session.commit()

    def sentiment_analysis(self, user_id: str, post_id: int):
        self.init_user_path(user_id, post_id)

        # with open(self.text_path, "r") as t:
        #     self.ocr_text_data = t.read()

        # ocr text db에서 가져오기
        ocr_text = Post.query.get(post_id).ocr_text
        self.ocr_text_data = ocr_text

        if self.request():
            self.save_response(post_id)


