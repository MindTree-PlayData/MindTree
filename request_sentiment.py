import requests
import json
import os
##### 요청 정보
url = 'https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze'
headers = {'X-NCP-APIGW-API-KEY-ID': os.environ.get("X_NCP_APIGW_API_KEY_ID"),
           'X-NCP-APIGW-API-KEY': os.environ.get("X_NCP_APIGW_API_KEY"),
           'Content-Type': 'application/json; charset=utf-8'
           }

def test01():
    print(os.environ.get("X_NCP_APIGW_API_KEY_ID"))

def read_text():
    with open("./data/sample_text02.txt", "r") as sample_text:
        text_data = sample_text.read()
    print(type(text_data))  # 스트링인 것을 확인
    return text_data


def request(text_data):
    """ - url: 요청보낼 url
        - headers: post요청 헤더에 담아야 할 정보.
            여기서는 key-id, secret key, content type을 담아야 한다.
        - json: body에 담을 컨텐츠. 분석할 내용에 해당. str타입이어야 한다.

        - .json() 은 응답받은 객체를 json으로 변환해준다."""

    res = requests.post(url=url,
                        headers=headers,
                        json={"content": text_data}
                        ).json()  # 응답을 json 형태로
    return res


def save_response(res):
    with open("./results/response02.json", "w", encoding='utf-8') as file:
        json.dump(res, file, indent='\t')


def load_response():
    with open("./results/response02.json", "r", ) as response:
        response_json = json.load(response)
        # print(response_json)

        for idx, sentence in enumerate(response_json['sentences']):
            print(f"\n{idx + 1}번")
            print(f"{sentence['content']}")
            print(f"{sentence['sentiment']}")
            print(f"{sentence['confidence']}")

        return response_json


if __name__ == "__main__":
    # text_data = read_text()
    # res = request(text_data)
    # save_response(res)
    load_response()
    # test01()