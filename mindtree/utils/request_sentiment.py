import requests
import os
import json

# 실행 경로에 따라 달라질 수 있어서 파일 경로를 기준으로 찾아가게 했음
key_path = os.path.join(os.path.dirname(__file__), "../../key/keys.json")
with open(key_path, "r") as keys:
    n_key = json.load(keys)


# 요청 정보
url = 'https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze'

headers = {'X-NCP-APIGW-API-KEY-ID': n_key["NAVER_API_KEY_ID"],
           'X-NCP-APIGW-API-KEY': n_key["NAVER_API_KEY"],
           'Content-Type': 'application/json; charset=utf-8'
           }


def read_text(user_id):
    """ 대상 id의 텍스트(ocr 결과)를 읽어온다. """
    text_path = os.path.join('results', str(user_id), str(user_id) + "_ocr.txt")
    with open(text_path, "r") as t:
        text_data = t.read()
    print(type(text_data))  # 스트링인 것을 확인
    return text_data


def request(text_data):
    """
    네이버 감성분석 API를 이용해 텍스트 데이터의 감성분석을 수행한다.
    :param text_data : 감성분석 할 텍스트 데이터 str

    :args for request
    - url: 요청보낼 url
    - headers: post요청 헤더에 담아야 할 정보.
        여기서는 key-id, secret key, content type을 담아야 한다.
    - json: body 에 담을 컨텐츠. 분석할 내용에 해당. str타입이어야 한다.
    - .json() 은 응답받은 객체를 json으로 변환해준다.
        그대로 두면 어떤 파이썬 객체로 반환되는 듯하다. """

    res = requests.post(url=url,
                        headers=headers,
                        json={"content": text_data}
                        )

    # res. status_code, json(), text, ...등을 쓸 수 있다.
    # json.loads(res.text) 로 써도 된다.

    res_json = json.loads(res.text)

    print(res_json)
    if res.status_code == 200:
        return res_json
    else:
        print(f"request error!{res.status_code}")
    return res_json


def save_response(res, user_id):
    """
    *** 계속 요청하면 횟수가 깎이므로 json 파일로 저장한다. ***
    :param res: Clova Sentiment analysis 반응 json 자료

    * 수정계획: 파일 이름을 user_id + text 정보 + [날짜정보] 를 포함하도록 함수를 구성할 것.
    """
    sentiment_path = os.path.join('results', str(user_id), str(user_id) + "_sentiment.json")
    with open(sentiment_path, "w", encoding='utf-8') as f:
        json.dump(res, f, indent='\t', ensure_ascii=False)


# def load_response():
#     """ 1. 저장된 json 파일을 가져온다.
#         2. 반응 json 파일을 출력한다."""
#
#     with open("../results/response02.json", "r") as response:
#         response_json = json.load(response)
#         # print(response_json)
#
#         for idx, sentence in enumerate(response_json['sentences']):
#             print(f"\n{idx + 1}번")
#             print(f"{sentence['content']}")
#             print(f"{sentence['sentiment']}")
#             print(f"{sentence['confidence']}")
#             print(f"{sentence['highlights']}")
#
#     return response_json


def sentiment_analysis(user_id):
    text_data = read_text(user_id)
    res = request(text_data)
    save_response(res, user_id)



if __name__ == "__main__":
    sentiment_analysis()
