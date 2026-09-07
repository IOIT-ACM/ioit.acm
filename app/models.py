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
    is_admin = db.Column(db.Boolean, default=False, nullable=False)


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


class Subscriber(db.Model):
    __bind_key__ = "users"
    __tablename__ = "subscribers"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class EmailLog(db.Model):
    __bind_key__ = "users"
    __tablename__ = "email_logs"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    template_used = db.Column(db.String(100), nullable=True)
    event_slugs = db.Column(db.Text, nullable=True)
    body_snapshot = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    sent_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipient_count = db.Column(db.Integer, nullable=False, default=0)

    sender = db.relationship("User", backref=db.backref("sent_email_logs", lazy=True))

