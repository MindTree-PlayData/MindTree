import json
import os
from threading import Thread

from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import secure_filename

from mindtree import app, db, bcrypt
from mindtree.models import User, Post
from mindtree.forms import RegistrationForm, LoginForm
from mindtree.thread import worker


# @app.route("/", methods=['GET'])
# def home():
#     """ 시작 페이지. 로그인을 할 수 있음."""
#     return render_template('login.html')


@app.route("/my_diary", methods=['GET'])
def my_diary():
    """ login required,  """
    return render_template('my_diary.html')


@app.route("/upload", methods=['GET'])
def upload():
    """ login required,  """
    return render_template('upload.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('my_diary'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("계정이 생성되었습니다. 로그인할 수 있습니다.", 'success')  # username으로 들어온 인풋을 data로 받을 수 있다.
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/",  methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print('form = LoginForm()')
    if form.validate_on_submit():
        print('form.validate_on_submit()')
        user = User.query.filter_by(email=form.email.data).first()

        # db의 password와 form의 password를 비교하여 True, False를 반환함
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print('user and bcrypt.check_password_hash(user.password, form.password.data)')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')  # arg: get method일때 주소에서 'next'키(key)에 대한 값(value)을 가져온다. 없으면 none
            '''
            예를 들어 /account 페이지에 접속했다가 로그인이 되어있지 않아서 /login으로 리디렉트 된 경우,
            주소가 http://127.0.0.1:5000/login?next=%2Faccount 과 같이 나온다.
            이 때 login에 성공하면, /home이 아니라 /account로 리디렉트 되도록 설정하는 것이다.
            '''
            return redirect(next_page) if next_page else redirect(url_for('my_diary'))
        else:
            flash('로그인 실패. email 또는 password를 다시 확인해 주세요.', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/login2", methods=['GET'])
def login2():
    """ login 로직을 수행함. 지금은 임시로 바로 my_diary로 보냄."""
    return redirect(url_for("my_diary"))


@app.route("/analyze", methods=['GET', 'POST'])
def analyze():
    """ login required,
    - 구현 방법
    analyze.html을 렌더 -> 렌더할 때 그래프에 들어갈 json data 전달 -> js 상에서 {{ userData }}로 받아 그래프를 그림

    :var user_id: str.
    :var sentiment_path: sentiment analysis 파일 저장 경로
    :var sentiment_json: json. sentiment analysis 결과 파일

    -- analyze 1:
        감성분석 bar graph. json 파일을 전달한다.
    -- analyze 2:
        word cloud. results 폴더 아래에 이미지 경로를 전달한다.
        - word_cloud 경로: results/<user_id>/<user_id>_word_cloud.png 이다.
        - 이때 results/ 가 media_folder로 정의되어 있다.
        - 따라서 이때 이미지가 저장된 경로에 접근하려면 <user_id>/<user_id>_word_cloud.png 를 전달하면 된다. """

    # -- analyze 1: 감성분석 bar graph
    user_id = request.form.get('id')  # 추후 로그인 시스템이 구축되면 세션 id를 받을 수 있도록 수정.
    print("user_id: ", user_id)
    sentiment_path = os.path.join('mindtree/results', str(user_id), str(user_id) + "_sentiment.json")
    with open(sentiment_path, "r",
              encoding="utf-8") as local_json:
        sentiment_json = json.load(local_json)

    # -- analyze 2: word cloud
    image_path = os.path.join(str(user_id), str(user_id) + "_word_cloud.png")

    return render_template('analyze.html', user_data=sentiment_json, image_path=image_path)


@app.route("/results/<path:filename>", methods=['GET'])
def get_file(filename):
    """ word cloud가 저장된 미디어 폴더에 접근한다. (results폴더)

    :param filename: results 폴더 아래부터의 이미지 경로
    :return: 지정된 directory의 파일에 접근한다.
    """
    media_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
    print("media_folder", media_folder)
    return send_from_directory(media_folder, filename)


@app.route("/upload_file", methods=['GET', 'POST'])
def upload_file():
    """
    1. 요청한 파일을 업로드 하고 my_diary로 리다이렉트 한다.
    2. OCR, text mining, sentiment analysis를 수행하도록 처리한다.
    """
    if request.method == "POST":
        # 요청한 파일을 업로드 한다.
        f = request.files['file']  # input 태그의 name 을 받음.

        # id 는 추후 로그인 시스템이 구현되면 세션에서 받아올 예정.
        user_id = request.form.get('id')
        print("user_id: ", user_id)

        # 경로 변수 정의
        filename = str(user_id) + '_' + str(secure_filename(f.filename))
        file_dir = os.path.join("mindtree/results", str(user_id))
        file_path = os.path.join(file_dir, filename)

        # 디렉토리 만들기
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir, exist_ok=True)

        # 이미지 저장
        f.save(file_path)

        # 현재 유저로 포스트를 db에 저장(빈 데이터를 저장하고, 각 분석이 끝나면 업데이트하는 방식)
        # post = Post(ocr_text="", sentiment={}, word_cloud="", authur=current_user)
        # db.session.add(post)
        # db.session.commit()
        flash("업로드에 성공하였습니다", "success")

        """ ** 업로드한 파일을 미리 분석해서 저장해둔다 **
        1. 1번이상 분석했다면, worker에 각 분석기가 초기화 되어 있으므로, 바로 분석함.
        2. 안되어있으면 초기화 후 분석 진행.
        단, app이 debug모드이기 때문에 reloading될 때마다 다시 초기화해야한다.
        """

        if worker.is_initialized():
            t1 = Thread(target=worker.analysis, args=[user_id])
            t1.start()
        else:
            t2 = Thread(target=worker.init_and_analyze, args=[user_id])
            t2.start()

        return redirect(url_for("my_diary"))

    else:
        return '실패'
