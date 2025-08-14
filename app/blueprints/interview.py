from flask import Blueprint, render_template


interviews_bp = Blueprint("interviews", __name__, template_folder="../templates")


@interviews_bp.route("/interviews/tenet-p1")
def home():
    return render_template("interviews/tenet.phase1.html")
