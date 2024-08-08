import logging

from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

# from .models import User
from web.auth.routes import AUTH_BP

from .auth.models import User
from .models import DB, Answer, Professional, Thread

APP_BP = Blueprint("app", __name__)

# ログイン用のエンドポイントを追加する
APP_BP.register_blueprint(AUTH_BP)


@APP_BP.route("/")
def index():
    # ログ出力の方法
    logging.debug("トップページにアクセスされました")
    # デフォルト:index.html を表示
    return render_template("index.html")


@APP_BP.route("/secret")
@login_required  # 画面デザイン中はコメントアウトしておくとよい (編集するたびにログインが切れてしまうため)
def secret():
    logging.debug("シークレットページにアクセスされました")
    # テンプレート内で直接 current_user を使わずに外から明示的に渡してあげると、画面デザ
    # イン時にダミーデータを渡すことができて便利

    # 例: 画面デザイン中
    # return render_template(
    #     "secret.html",
    #     user=User(
    #         username="test_user",
    #         hashed_password="dummy_value",
    #     ),
    # )

    # 画面デザイン完了後、動作確認中
    return render_template("secret.html", user=current_user)


@APP_BP.route("/top_page")
def top_page():
    logging.debug("新しいトップページにアクセスされました")
    # 未解決のスレッドを取得
    unsolved_threads = DB.session.query(Thread).filter(Thread.solve == 0).all()
    # 解決済みのスレッドを取得
    solved_threads = DB.session.query(Thread).filter(Thread.solve == 1).all()
    return render_template(
        "top_page.html",
        unsolved_threads=unsolved_threads,
        solved_threads=solved_threads,
    )


@APP_BP.route("/login")
def login():
    logging.debug("ログインページにアクセスされました")
    return render_template("login.html")


@APP_BP.route("/signup")
def signup():
    logging.debug("サインアップページにアクセスされました")
    return render_template("signup.html")


@APP_BP.route("/form")
def form():
    logging.debug("フォームページにアクセスされました")
    return render_template("form.html")


@APP_BP.route("/answer")
def answer():
    logging.debug("回答ページにアクセスされました")
    return render_template("answer.html")


@APP_BP.route("/delogin_answer")
def delogin_answer():
    logging.debug("回答ページにアクセスされました")
    return render_template("delogin_answer.html")


@APP_BP.route("/my_top_page")
@login_required  # 画面デザイン中はコメントアウトしておくとよい (編集するたびにログインが切れてしまうため)
def my_top_page():
    logging.debug("マイトップページにアクセスされました")
    unsolved_threads = DB.session.query(Thread).filter(Thread.solve == 0).all()
    # 解決済みのスレッドを取得
    solved_threads = DB.session.query(Thread).filter(Thread.solve == 1).all()
    return render_template(
        "my_top_page.html",
        user=current_user,
        unsolved_threads=unsolved_threads,
        solved_threads=solved_threads,
    )


# @APP_BP.route("/answer")
# @login_required
# def answer():
#     logging.debug("回答ページにアクセスされました")
#     return render_template("answer.html")


# 全ての質問スレッドを取得するエンドポイントを追加する
@APP_BP.route("/api/v1/all_threads", methods=["GET"])
# @login_required
def get_all_threads():
    threads = DB.session.query(
        Thread.thread_id,
        Thread.title,
        Thread.description,
        Thread.solve,
        Thread.created_date,
        Thread.updated_date,
    ).all()
    target_threads = func_like_threads_schema(threads)
    return jsonify(target_threads)


def func_like_threads_schema(threads):
    target_threads = [
        {
            "thread_id": thread.thread_id,
            "user_id": thread.user_id,
            "title": thread.title,
            "description": thread.description,
            "solve": thread.solve,
            "created_date": thread.created_date,
            "updated_date": thread.updated_date,
        }
        for thread in threads
    ]
    return target_threads


# 指定された質問idの質問の取得
@APP_BP.route("/questions/<int:thread_id>", methods=["GET"])
def get_question_by_id(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    result = {"title": thread.title, "description": thread.description}
    return jsonify(result)


@APP_BP.route("/api/v1/all_professionals", methods=["GET"])
# @login_required
def get_all_professionals():
    professionals = DB.session.query(
        Professional.professional_id,
        Professional.profession,
    ).all()
    target_professionals = func_like_professionals_schema(professionals)
    return jsonify(target_professionals)


def func_like_professionals_schema(professionals):
    target_professionals = [
        {
            "professional_id": professional.professional_id,
            "profession": professional.profession,
        }
        for professional in professionals
    ]
    return target_professionals


@APP_BP.route("/api/v1/all_users", methods=["GET"])
# @login_required
def get_all_users():
    users = DB.session.query(
        User.id, User.username, User.hashed_password, User.professional
    ).all()
    target_users = func_like_users_schema(users)
    return jsonify(target_users)


def func_like_users_schema(users):
    target_users = [
        {
            "id": user.id,
            "username": user.username,
            "hashed_password": user.hashed_password,
            "professional": user.professional,
        }
        for user in users
    ]
    return target_users


@APP_BP.route("/api/v1/all_answers", methods=["GET"])
# @login_required
def get_all_answers():
    answers = DB.session.query(
        Answer.answer_id,
        Answer.thread_id,
        Answer.user_id,
        Answer.description,
        Answer.created_date,
        Answer.updated_date,
    ).all()
    target_answers = func_like_answers_schema(answers)
    return jsonify(target_answers)


def func_like_answers_schema(answers):
    target_answers = [
        {
            "answer_id": answer.answer_id,
            "thread_id": answer.thread_id,
            "user_id": answer.user_id,
            "description": answer.description,
            "created_date": answer.created_date,
            "updated_date": answer.updated_date,
        }
        for answer in answers
    ]
    return target_answers


@APP_BP.route("/api/v1/user/<int:user_id>/professional", methods=["GET"])
# @login_required
def get_user_professional(user_id):
    user = DB.session.query(User.professional).filter(User.id == user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"professional": user.professional})


@APP_BP.route("/api/v1/all_threads", methods=["GET"])
# @login_required
def get_threads():
    threads = DB.session.query(
        Thread.thread_id, Thread.title, Thread.description, Thread.solve
    ).all()
    target_threads = func_like_threads_schema(threads)
    return jsonify(target_threads)


def func_like_thread_schema(threads):
    target_threads = [
        {
            "thread_id": thread.thread_id,
            "title": thread.title,
            "description": thread.description,
            "solve": thread.solve,
        }
        for thread in threads
    ]
    return target_threads


# 新規質問(質問タイトル、本文、タグ、解決済み)の作成
@APP_BP.route("/api/v1/create_new_thread/<user_id>", methods=["POST"])
def create_new_thread(user_id):
    #     if request.content_type != "application/json":
    #         return jsonify({"error": "Content-Type must be application/json"}), 415
    # ユーザーがいるか確認する処理
    new_thread = Thread(
        user_id=user_id,
        title=request.json["title"],
        description=request.json["description"],
        solve=0,
    )
    DB.session.add(new_thread)
    DB.session.commit()
    return jsonify(func_like_threads_schema([new_thread]))


# 新規回答文(質問id、回答文)の作成
@APP_BP.route("/api/v1/create_new_answer/<thread_id>", methods=["POST"])
def create_new_answer(thread_id):
    # ユーザーがいるか確認する処理
    new_answer = Answer(
        thread_id=thread_id,
        user_id=request.json["user_id"],
        description=request.json["description"],
    )
    DB.session.add(new_answer)
    DB.session.commit()
    return jsonify(func_like_answer_schema([new_answer]))


def func_like_answer_schema(answers):
    target_answers = [
        {
            "thread_id": answer.thread_id,
            "user_id": answer.user_id,
            "description": answer.description,
        }
        for answer in answers
    ]
    return target_answers


# 職種データの登録
@APP_BP.route("/api/v1/", methods=["POST"])
def create_new_profession(thread_id):
    # ユーザーがいるか確認する処理
    new_profession = Professional(
        professional_id=request.json["professional_id"],
        Profession=request.json["profession"],
    )
    DB.session.add(new_profession)
    DB.session.commit()
    return jsonify(func_like_professinal_schema([new_profession]))


def func_like_professinal_schema(profession):
    target_profession = [
        {
            "thread_id": answer.thread_id,
            "user_id": answer.user_id,
            "description": answer.description,
        }
        for answer in profession
    ]
    return target_profession
