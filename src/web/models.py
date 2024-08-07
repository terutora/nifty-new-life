from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TINYINT as Tinyint

DB = SQLAlchemy()
MIGRATE = Migrate()


class Professional(DB.Model):
    professional_id = DB.Column(DB.Integer, primary_key=True)
    profession = DB.Column(DB.String(50))


class Thread(DB.Model):
    thread_id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey("user.id"))
    title = DB.Column(DB.String(50))
    description = DB.Column(DB.String(50))
    solve = DB.Column(Tinyint(1))
    created_date = DB.Column(DB.DateTime, nullable=False, default=datetime.now)
    updated_date = DB.Column(
        DB.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )


class Answer(DB.Model):
    answer_id = DB.Column(DB.Integer, primary_key=True)
    thread_id = DB.Column(DB.Integer, DB.ForeignKey("thread.thread_id"))
    user_id = DB.Column(DB.Integer)
    description = DB.Column(DB.String(50))
    created_date = DB.Column(DB.DateTime, nullable=False, default=datetime.now)
    updated_date = DB.Column(
        DB.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
