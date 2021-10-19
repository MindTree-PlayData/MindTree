import json
import os
from threading import Thread

from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import secure_filename
from mindtree import app, db, bcrypt, USER_BASE_PATH
from mindtree.models import User, Post
from mindtree.forms import RegistrationForm, LoginForm
from mindtree.thread import worker


@app.route("/my_diary", methods=['GET'])
def my_diary():
    """ login required,  """
    username = current_user.username
    posts = Post.query.filter_by(author=current_user).all()
    print("my_diary(): ", username)
    # print("my_diary: ", posts)  # post 쿼리 확인.
    return render_template('my_diary.html', posts=posts)


@app.route("/upload", methods=['GET'])
def upload():
    """ login required,  """
    user = current_user.get_id()
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

            return redirect(next_page) if next_page else redirect(url_for('my_diary'))
        else:
            flash('로그인 실패. email 또는 password를 다시 확인해 주세요.', 'danger')
    return render_template('login.html', title='login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/analyze/<int:post_id>')
def analyze(post_id):
    """
    - 해당 포스트 아이디로 쿼리 후 결과가 없으면 보내지 않게 하기 """

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    username = User.query.get(user_id).username

    sentiment_json = post.sentiment  # 감성분석 json 데이터
    word_cloud = post.word_cloud  # 워드클라우드 파일 이름

    image_path = os.path.join(str(username), word_cloud)
    print(image_path)

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
        title = request.form.get('title')
        # 요청한 파일을 업로드 한다.
        f = request.files['file']  # input 태그의 name 을 받음.
        print("f", f.filename)

        # 현재 로그인된 유저의 username을 가져온다.
        user_id: str = current_user.username
        print("user_id: ", user_id)

        # 현재 유저로 포스트를 db에 저장(빈 데이터를 저장하고, 각 분석이 끝나면 업데이트하는 방식)
        post = Post(title="", ocr_text=title, sentiment={}, word_cloud="", author=current_user)
        db.session.add(post)
        db.session.commit()
        post_id: int = post.id

        # 경로 변수 정의
        filename = f"{user_id}_{str(post_id)}.png"
        file_dir = os.path.join(USER_BASE_PATH, user_id)
        file_path = os.path.join(file_dir, filename)

        # 디렉토리 만들기
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir, exist_ok=True)

        # 이미지 저장
        f.save(file_path)

        flash("업로드에 성공하였습니다", "success")

        """ ** 업로드한 파일을 미리 분석해서 저장해둔다 **
        1. 1번이상 분석했다면, worker에 각 분석기가 초기화 되어 있으므로, 바로 분석함.
        2. 안되어있으면 초기화 후 분석 진행.
        단, app이 debug모드이기 때문에 reloading될 때마다 다시 초기화해야한다.
        """

        if worker.is_initialized():
            t1 = Thread(target=worker.analysis, args=[user_id, post_id])
            t1.start()
        else:
            t2 = Thread(target=worker.init_and_analyze, args=[user_id, post_id])
            t2.start()

        return redirect(url_for("my_diary"))

    else:
        return '실패'


@app.template_filter('datetime')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime('%Y년 %m월 %d일')
