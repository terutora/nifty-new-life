import logging

from flask import Blueprint, jsonify, render_template
from flask_login import current_user, login_required

from web.auth.models import User

# from .models import User
from web.auth.routes import AUTH_BP
from web.models import DB, Answer, Professional, Thread

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
    return render_template("top_page.html")


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


@APP_BP.route("/my_top_page")
@login_required  # 画面デザイン中はコメントアウトしておくとよい (編集するたびにログインが切れてしまうため)
def my_top_page():
    logging.debug("マイトップページにアクセスされました")
    return render_template("my_top_page.html", user=current_user)


# @APP_BP.route("/answer")
# @login_required
# def answer():
#     logging.debug("回答ページにアクセスされました")
#     return render_template("answer.html")


# 全ての質問スレッドを取得するエンドポイントを追加する
@APP_BP.route("/api/v1/all_threads")
# @login_required
def get_all_threads():
    threads = DB.session.query(
        Thread.thread_id, Thread.title, Thread.description, Thread.solve
    ).all()
    target_threads = func_like_threads_schema(threads)
    return jsonify(target_threads)


def func_like_threads_schema(threads):
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


# 指定された質問idの質問の取得
@APP_BP.route("/questions/<int:thread_id>", methods=["GET"])
def get_question_by_id(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    result = {"title": thread.title, "description": thread.description}
    return jsonify(result)
