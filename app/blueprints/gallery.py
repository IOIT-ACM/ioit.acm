from flask import Blueprint, render_template

gallery_bp = Blueprint("gallery", __name__, template_folder="../templates")


@gallery_bp.route("/gallery")
def home():
    return render_template("gallery.html")
