from flask import Blueprint, render_template

join_bp = Blueprint("join", __name__, template_folder="../templates")


@join_bp.route("/join")
def team():
    return render_template(
        "join.html",
    )
