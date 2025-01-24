from flask import Blueprint, jsonify, render_template
from app import db
from ...models import *
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


@competitions_bp.route("/leaderboard/bitbyquery_jan2025")
def BitByQueryleaderboard():
    leaderboard = [
        {"username": "8273519", "name": "Mahi Kulkarni", "problems_solved": 80, "score": 598},
        {"username": "5785996", "name": "Anushka Gaikwad", "problems_solved": 53, "score": 368},
        {"username": "2104080", "name": "Om Chavan", "problems_solved": 48, "score": 338},
        {"username": "7276229611", "name": "Prathvish Shetty", "problems_solved": 47, "score": 336},
        {"username": "5302819", "name": "Parth Dhengle", "problems_solved": 46, "score": 322},
        {"username": "6443616", "name": "Devika Yogiraj Mule", "problems_solved": 42, "score": 294},
        {"username": "5635415", "name": "Pankaj Jagadale", "problems_solved": 41, "score": 290},
        {"username": "1070907", "name": "Raghav", "problems_solved": 41, "score": 284},
        {"username": "0286642", "name": "Pratik Santosh Karande", "problems_solved": 39, "score": 280},
        {"username": "2636682", "name": "Yash Inamdar", "problems_solved": 34, "score": 250},
        {"username": "8767630109", "name": "Sanjana Godse", "problems_solved": 31, "score": 210},
        {"username": "9080543", "name": "Suraj Prabhakar Gharde", "problems_solved": 30, "score": 210},
        {"username": "4242217", "name": "Avdhoot Chavan", "problems_solved": 28, "score": 208},
        {"username": "5918582", "name": "Sakshi Mane", "problems_solved": 27, "score": 192},
        {"username": "2003", "name": "Yashraj Dhamale", "problems_solved": 25, "score": 178},
        {"username": "7385234057", "name": "Devang Gandhi", "problems_solved": 19, "score": 134},
        {"username": "7442881", "name": "Bhavna Sharadchandra Datal", "problems_solved": 18, "score": 112},
        {"username": "141209", "name": "Jayesh Ingale", "problems_solved": 13, "score": 102},
        {"username": "8077480", "name": "Bhumi Boinwad", "problems_solved": 12, "score": 76},
        {"username": "1189277", "name": "aarti datal", "problems_solved": 11, "score": 68},
        {"username": "9280933", "name": "Priya Chakane", "problems_solved": 9, "score": 56},
        {"username": "8523812", "name": "sahil ghate", "problems_solved": 7, "score": 48},
        {"username": "aaaa", "name": "pranita", "problems_solved": 1, "score": 8},
    ]
    return render_template(
        "leaderboards/bitbyquery_jan2025.html",
        leaderboard=leaderboard,
        user=current_user,
    )


@competitions_bp.route("/leaderboard/virtual_contest_bitbyquery_jan2025")
def VirtualContest_leaderboard():
    leaderboard = [
        {"id": 1, "username": "swaroop123", "name": "Swaroop Patil", "problems_solved": 10, "total_time": "7:11"},
        {"id": 2, "username": "123456", "name": "online", "problems_solved": 10, "total_time": "15:03"},
        {"id": 3, "username": "0561552", "name": "Virendra Avinash Kharate", "problems_solved": 10, "total_time": "29:25"},
        {"id": 4, "username": "65432", "name": "Anshu", "problems_solved": 10, "total_time": "30:20"},
        {"id": 5, "username": "2104080", "name": "Om Anandrao Chavan", "problems_solved": 9, "total_time": "14:29"},
        {"id": 6, "username": "8418690", "name": "Vaishnav Tanaji Kokate", "problems_solved": 9, "total_time": "19:47"},
        {"id": 7, "username": "acm123", "name": "Vilgax", "problems_solved": 8, "total_time": "6:53"},
        {"id": 8, "username": "81181888", "name": "Ganesh Matole", "problems_solved": 7, "total_time": "13:16"},
        {"id": 9, "username": "7991427", "name": "Sarthak Deochake", "problems_solved": 7, "total_time": "18:58"},
        {"id": 10, "username": "12341234", "name": "lmao", "problems_solved": 6, "total_time": "13:55"},
        {"id": 11, "username": "grey", "name": "Grey Matter", "problems_solved": 5, "total_time": "3:47"},
        {"id": 12, "username": "thanos123", "name": "Thanos", "problems_solved": 4, "total_time": "2:54"},
        {"id": 13, "username": "1234567890", "name": "Virat Kohli", "problems_solved": 4, "total_time": "14:38"},
        {"id": 14, "username": "abc", "name": "abc", "problems_solved": 3, "total_time": "2:27"},
        {"id": 15, "username": "5651925", "name": "Vibhawari Sasane", "problems_solved": 3, "total_time": "3:02"},
        {"id": 16, "username": "2813964", "name": "Devang Gandhi", "problems_solved": 3, "total_time": "5:49"},
        {"id": 17, "username": "user456", "name": "Ben Tennyson", "problems_solved": 3, "total_time": "11:17"},
        {"id": 18, "username": "shriya123", "name": "shriya", "problems_solved": 2, "total_time": "0:50"},
        {"id": 19, "username": "123", "name": "ABC", "problems_solved": 2, "total_time": "3:28"},
        {"id": 20, "username": "9260366", "name": "Aditya Godse", "problems_solved": 2, "total_time": "4:38"},
        {"id": 21, "username": "5918582", "name": "Sakshi Mane", "problems_solved": 2, "total_time": "9:47"},
        {"id": 22, "username": "5522283", "name": "Ashish Kharde", "problems_solved": 1, "total_time": "2:24"},
    ]
    return render_template(
        "leaderboards/virtual_contest_bitbyquery_jan2025.html",
        leaderboard=leaderboard,
        user=current_user,
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
