from flask import Blueprint, render_template
from app.data.projects import projects_data


projects_bp = Blueprint("projects", __name__, template_folder="../templates")


@projects_bp.route("/projects")
def home():
    return render_template("projects.html", projects=projects_data)
