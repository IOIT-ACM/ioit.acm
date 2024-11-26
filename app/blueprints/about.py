from flask import Blueprint, render_template

about_bp = Blueprint("abour", __name__, template_folder="../templates")


@about_bp.route("/about")
def home():
    return render_template("about.html")
