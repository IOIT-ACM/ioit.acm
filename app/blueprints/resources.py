from flask import Blueprint, render_template
from app.data.resources import resource_data

resources_bp = Blueprint("resources", __name__, template_folder="../templates")


@resources_bp.route("/resources")
def index():
    return render_template("resources.html", categories=resource_data)
