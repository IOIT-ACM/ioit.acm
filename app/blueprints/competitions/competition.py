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

@competitions_bp.route("/leaderboard/bitbyquery_aug2025")
def bitbyquery_aug2025_leaderboard():
    leaderboard = [
        {"username": "8273519", "name": "Mahi Kulkarni", "problems_solved": 65, "score": 483, "last_submission": "Aug 26, 2025, 3:27:47 PM"},
        {"username": "5785996", "name": "Anushka Gaikwad", "problems_solved": 57, "score": 416, "last_submission": "Aug 26, 2025, 3:29:40 PM"},
        {"username": "7925080", "name": "Bhavesh Dhanvij", "problems_solved": 50, "score": 359, "last_submission": "Aug 26, 2025, 3:28:11 PM"},
        {"username": "3967983", "name": "Shivendra Bhaginath Devadhe", "problems_solved": 48, "score": 354, "last_submission": "Aug 26, 2025, 3:29:05 PM"},
        {"username": "8867966", "name": "Tanishka Gadilkar", "problems_solved": 44, "score": 317, "last_submission": "Aug 26, 2025, 3:29:12 PM"},
        {"username": "286642", "name": "Pratik Karande", "problems_solved": 40, "score": 292, "last_submission": "Aug 26, 2025, 3:29:38 PM"},
        {"username": "108036", "name": "Raj Gaikwad", "problems_solved": 40, "score": 291, "last_submission": "Aug 26, 2025, 3:27:24 PM"},
        {"username": "24410003", "name": "Parth Kiran Agre", "problems_solved": 36, "score": 265, "last_submission": "Aug 26, 2025, 3:29:02 PM"},
        {"username": "9014695", "name": "Purva Rajendra Patil", "problems_solved": 35, "score": 249, "last_submission": "Aug 26, 2025, 3:20:29 PM"},
        {"username": "5918582", "name": "Sakshi Mane", "problems_solved": 34, "score": 244, "last_submission": "Aug 26, 2025, 3:26:45 PM"},
        {"username": "9988997", "name": "Prathmesh Dasarwar", "problems_solved": 32, "score": 223, "last_submission": "Aug 26, 2025, 3:26:15 PM"},
        {"username": "8693975", "name": "Anushka Maurya", "problems_solved": 29, "score": 208, "last_submission": "Aug 26, 2025, 3:26:34 PM"},
        {"username": "4819284", "name": "Harshali Patil", "problems_solved": 29, "score": 207, "last_submission": "Aug 26, 2025, 3:26:48 PM"},
        {"username": "1500397", "name": "Amit Parmeshwar Dhuttaragi", "problems_solved": 28, "score": 194, "last_submission": "Aug 26, 2025, 3:29:13 PM"},
        {"username": "2813964", "name": "Devang Gandhi", "problems_solved": 26, "score": 188, "last_submission": "Aug 26, 2025, 3:27:05 PM"},
        {"username": "5547800", "name": "Bhargavi Sandeep Tambe", "problems_solved": 23, "score": 158, "last_submission": "Aug 26, 2025, 3:24:07 PM"},
        {"username": "5343003", "name": "Srushti Mule", "problems_solved": 20, "score": 143, "last_submission": "Aug 26, 2025, 3:24:55 PM"},
        {"username": "23510067", "name": "Devika Mule", "problems_solved": 14, "score": 100, "last_submission": "Aug 26, 2025, 2:10:57 PM"},
        {"username": "6863984", "name": "Kshitij Sharad Kumavat", "problems_solved": 13, "score": 89, "last_submission": "Aug 26, 2025, 3:29:39 PM"},
        {"username": "7143281", "name": "Govinda Shinde", "problems_solved": 12, "score": 79, "last_submission": "Aug 26, 2025, 3:22:09 PM"},
        {"username": "23510058", "name": "Bhumi Ganesh Shinde", "problems_solved": 11, "score": 76, "last_submission": "Aug 26, 2025, 3:24:34 PM"},
        {"username": "9631773", "name": "Rushikesh Saheb Mundaware", "problems_solved": 9, "score": 68, "last_submission": "Aug 26, 2025, 3:23:48 PM"},
        {"username": "Shubham", "name": "Shubham Shinde", "problems_solved": 8, "score": 57, "last_submission": "Aug 26, 2025, 3:29:24 PM"},
        {"username": "7955918", "name": "Riya Nilesh Laddha", "problems_solved": 8, "score": 51, "last_submission": "Aug 26, 2025, 3:25:48 PM"},
        {"username": "24610031", "name": "Tanay Gawari", "problems_solved": 3, "score": 24, "last_submission": "Aug 26, 2025, 3:27:59 PM"},
        {"username": "5163826", "name": "Yashwant Nandkishor Wankhede", "problems_solved": 3, "score": 22, "last_submission": "Aug 26, 2025, 3:21:59 PM"},
        {"username": "test", "name": "test", "problems_solved": 2, "score": 18, "last_submission": "Aug 26, 2025, 3:08:39 PM"},
        {"username": "8591196", "name": "Atharv Pednekar", "problems_solved": 2, "score": 16, "last_submission": "Aug 26, 2025, 2:19:42 PM"},
        {"username": "24510090", "name": "Shravani Yogesh Pardeshi", "problems_solved": 2, "score": 16, "last_submission": "Aug 26, 2025, 2:27:50 PM"},
    ]
    return render_template(
        "leaderboards/bitbyquery.html",
        leaderboard=leaderboard,
        title="Bit By Query Vol. 2 AUG 2025",
        date="26 August 2025",
        event_link="/events/Bit%20By%20Query%20-%20Vol%202",
        user=current_user,
    )

@competitions_bp.route("/leaderboard/bitbyquery_jan2025")
def bitbyquery_jan2025_leaderboard():
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
        "leaderboards/bitbyquery.html",
        leaderboard=leaderboard,
        title="Bit By Query Vol. 1 JAN 2025",
        date="24 January 25",
        event_link="/events/Bit%20By%20Query%20-%20Vol%201",
        user=current_user,
    )

@competitions_bp.route("/leaderboard/virtual_contest_bitbyquery_jan2025")
def virtual_contest_bitbyquery_jan2025():
    leaderboard = [
        {"username": "swaroop123", "name": "Swaroop Patil", "problems_solved": 10, "total_time": "7:11"},
        {"username": "123456", "name": "online", "problems_solved": 10, "total_time": "15:03"},
        {"username": "0561552", "name": "Virendra Avinash Kharate", "problems_solved": 10, "total_time": "29:25"},
        {"username": "65432", "name": "Anshu", "problems_solved": 10, "total_time": "30:20"},
        {"username": "2104080", "name": "Om Anandrao Chavan", "problems_solved": 9, "total_time": "14:29"},
        {"username": "8418690", "name": "Vaishnav Tanaji Kokate", "problems_solved": 9, "total_time": "19:47"},
        {"username": "acm123", "name": "Vilgax", "problems_solved": 8, "total_time": "6:53"},
        {"username": "81181888", "name": "Ganesh Matole", "problems_solved": 7, "total_time": "13:16"},
        {"username": "7991427", "name": "Sarthak Deochake", "problems_solved": 7, "total_time": "18:58"},
        {"username": "12341234", "name": "lmao", "problems_solved": 6, "total_time": "13:55"},
        {"username": "grey", "name": "Grey Matter", "problems_solved": 5, "total_time": "3:47"},
        {"username": "thanos123", "name": "Thanos", "problems_solved": 4, "total_time": "2:54"},
        {"username": "1234567890", "name": "Virat Kohli", "problems_solved": 4, "total_time": "14:38"},
        {"username": "abc", "name": "abc", "problems_solved": 3, "total_time": "2:27"},
        {"username": "5651925", "name": "Vibhawari Sasane", "problems_solved": 3, "total_time": "3:02"},
        {"username": "2813964", "name": "Devang Gandhi", "problems_solved": 3, "total_time": "5:49"},
        {"username": "user456", "name": "Ben Tennyson", "problems_solved": 3, "total_time": "11:17"},
        {"username": "shriya123", "name": "shriya", "problems_solved": 2, "total_time": "0:50"},
        {"username": "123", "name": "ABC", "problems_solved": 2, "total_time": "3:28"},
        {"username": "9260366", "name": "Aditya Godse", "problems_solved": 2, "total_time": "4:38"},
        {"username": "5918582", "name": "Sakshi Mane", "problems_solved": 2, "total_time": "9:47"},
        {"username": "5522283", "name": "Ashish Kharde", "problems_solved": 1, "total_time": "2:24"},
    ]
    return render_template(
        "leaderboards/bitbyquery.html",
        leaderboard=leaderboard,
        title="Virtual Contest - Bit By Query JAN 2025",
        date="24 January 25",
        event_link="/events/Virtual%20Contest%20-%20Bit%20By%20Query%20Vol%201",
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
        {"name": "Bit by Query - Vol 2", "date": "2025-08-26"}
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
