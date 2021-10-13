import requests
import os
import json
from mindtree import USER_BASE_PATH

USER_BASE_PATH = '/Users/motive/Data_Study/Projects/MindTree/mindtree/results/'
user_id = 'toptoptop'

key_path = os.path.join(os.path.dirname(__file__), "../../key/keys.json")
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

    def init_user_path(self, user_id) -> None:
        self.text_path = os.path.join(USER_BASE_PATH, str(user_id), str(user_id) + "_ocr.txt")
        self.sentiment_path = os.path.join(USER_BASE_PATH, str(user_id), str(user_id) + "_sentiment.json")

    def request(self):
        self.res = requests.post(url=self.url,
                                 headers=self.headers,
                                 json={"image_content": self.ocr_text_data}
                                 )
        self.json_response = self.res.json()

        if self.res.status_code == 200:
            return self.json_response
        else:
            print(f"request error!{self.res.status_code}")

        return self.json_response

    def save_response(self) -> None:
        with open(self.sentiment_path, "w", encoding='utf-8') as f:
            json.dump(self.json_response, f, indent='\t', ensure_ascii=False)

    def sentiment_analysis(self, user_id: str):
        self.init_user_path(user_id)
        with open(self.text_path, "r") as t:
            self.ocr_text_data = t.read()
        self.request()
        self.save_response()

