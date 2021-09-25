from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from werkzeug.utils import secure_filename
from utils.OCR import ocr
import os
import json

app = Flask(__name__)
"""로컬 환경에서 자바스크립트로 flask 도메인에 요청하는 경우, CORS 에러 발생.
    즉, 동일 출처가 아닐 때 에러가 발생하는데, 이를 해결해주는 flask_cors 를 사용한다.
    https://webisfree.com/2020-01-01/python-flask%EC%97%90%EC%84%9C-cors-cross-origin-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0 """
CORS(app)
app.secret_key = "donkey_secret"  # flash 쓰려면 설정해야함.


@app.route("/", methods=['GET'])
def home():
    return render_template('upload.html')


@app.route("/result", methods=['GET'])
def result():
    """ login required,  """
    return render_template('index.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        # 요청한 파일을 업로드 한다.
        f = request.files['file']  # input 태그의 name 을 받음.
        user_id = request.form.get('id')
        filename = secure_filename(f.filename)
        filepath = os.path.join("./static/images/" + str(user_id) + '_' + str(filename))
        f.save(filepath)
        flash("업로드에 성공하였습니다", "success")

        ### 업로드한 파일을 미리 분석해서 저장해둔다.  ###
        # request OCR
        ocr_result = ocr(filepath, user_id)
        print(ocr_result)
        # text mining

        # sentiment analysis

        return render_template("my_diary.html")

    else:
        return '실패'


@app.route("/json_data", methods=['GET', 'POST'])
def json_data():
    with open("/Users/motive/Data_Study/Projects/MindTree/results/response02.json", "r",
              encoding="utf-8") as local_json:
        data = json.load(local_json)
    print(data)
    return data


if __name__ == "__main__":
    app.run(debug=True)