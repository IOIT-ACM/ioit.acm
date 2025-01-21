from flask import Blueprint, jsonify, render_template
from app import db
from ...models import GlobalLeaderboard, Question
from flask_login import current_user
from datetime import datetime

now = datetime.now()

competitions_bp = Blueprint("competitions", __name__)


###
### Competitions Home
###
@competitions_bp.route("/competitions")
def competitions():
    return render_template("competitions/home.html", user=current_user, now=now)


# @competitions_bp.route('/competitions/jan2025')
# def competition_jan2025():
#     app = db.get_app()
#     app.config['SQLALCHEMY_BINDS']['questions'] = 'sqlite:///instance/competitions/jan2025/questions.db'

#     questions = Question.query.all()
#     return jsonify([{"id": q.id, "text": q.question_text} for q in questions])


###
### leaderboard
###
@competitions_bp.route("/leaderboard")
def global_leaderboard():
    leaderboard = GlobalLeaderboard.query.order_by(GlobalLeaderboard.score.desc()).all()
    user_branches = sorted(set(entry.branch for entry in leaderboard))
    return render_template(
        "competitions/leaderboard.html",
        leaderboard=leaderboard,
        user=current_user,
        user_branches=user_branches,
    )


@competitions_bp.route("/leaderboard/jan2025")
def competition_leaderboard():
    return global_leaderboard()


###
### Virtual Contest
###
@competitions_bp.route("/competitions/virtualcontest")
def virtualcontest():
    return render_template("competitions/index/virtualcontest.html", user=current_user)


###
### Competitions
###
@competitions_bp.route("/competitions/bit-by-bit")
def bitbybit():
    events = [
        {"name": "Bit by Bit - Vol 1", "date": "2025-01-21"},
        {"name": "Bit by Bit", "date": "2024-03-15"},
        {"name": "Bit by Bit", "date": "2024-04-20"},
        {"name": "Bit by Bit", "date": "2024-05-25"},
        {"name": "Bit by Bit", "date": "2024-01-10"},
        {"name": "Bit by Bit", "date": "2024-02-14"},
    ]

    upcoming_events = [
        event for event in events if datetime.strptime(event["date"], "%Y-%m-%d") > now
    ]
    past_events = [
        event for event in events if datetime.strptime(event["date"], "%Y-%m-%d") <= now
    ]

    return render_template(
        "competitions/index/bit-by-bit.html",
        user=current_user,
        upcoming_events=upcoming_events,
        past_events=past_events,
    )


@competitions_bp.route("/competitions/bit-by-query")
def bitbyquery():
    events = [
        {"name": "Bit by Query - Vol 1", "date": "2025-01-24"},
    ]

    upcoming_events = [
        event for event in events if datetime.strptime(event["date"], "%Y-%m-%d") > now
    ]
    past_events = [
        event for event in events if datetime.strptime(event["date"], "%Y-%m-%d") <= now
    ]

    return render_template(
        "competitions/index/bit-by-query.html",
        user=current_user,
        upcoming_events=upcoming_events,
        past_events=past_events,
    )


@competitions_bp.route("/competitions/ml-frontiers")
def mlfrontiers():
    events = []

    upcoming_events = [
        event for event in events if datetime.strptime(event["date"], "%Y-%m-%d") > now
    ]
    past_events = [
        event for event in events if datetime.strptime(event["date"], "%Y-%m-%d") <= now
    ]
    return render_template(
        "competitions/index/ml-frontiers.html",
        user=current_user,
        upcoming_events=upcoming_events,
        past_events=past_events,
    )
