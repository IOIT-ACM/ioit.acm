from flask import Blueprint, render_template

from app.data.teams import team_data

about_bp = Blueprint("abour", __name__, template_folder="../templates")


@about_bp.route("/about")
def home():
    latest_year = max(team_data)
    return render_template("about.html", leadership=team_data[latest_year])
