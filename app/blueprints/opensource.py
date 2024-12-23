from flask import Blueprint, render_template

opensource_bp = Blueprint("opensource", __name__, template_folder="../templates")


@opensource_bp.route("/opensource")
def team():
    return render_template(
        "opensource.html",
    )
