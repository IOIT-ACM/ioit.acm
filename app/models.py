from app import db
from flask_login import UserMixin
from app.db import db


class User(db.Model, UserMixin):
    __bind_key__ = "users"
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    acm_id = db.Column(db.String(150), unique=False, nullable=True)
    mobile_no = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    completed_competitions = db.Column(db.Integer, default=0)


class GlobalLeaderboard(db.Model):
    __bind_key__ = "global_leaderboard"
    __tablename__ = "global_leaderboard"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    branch = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer, default=0)


class VirtualContest(db.Model):
    __bind_key__ = "global_leaderboard"
    __tablename__ = "virtual_contest"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer, default=0)
    solved_questions = db.Column(db.String(50), nullable=False)
    time_taken = db.Column(db.Float, nullable=False)


class Question(db.Model):
    __bind_key__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    correct_answer = db.Column(db.Text, nullable=False)


class VirtualContestBitByQueryJan2025(db.Model):
    __bind_key__ = "global_leaderboard"
    __tablename__ = "virtual_contest_bitbyquery_jan2025"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    problems_solved = db.Column(db.Integer, nullable=False, default=0)
    total_time = db.Column(db.Float, nullable=False, default=0.0)
