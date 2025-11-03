from flask import Blueprint, render_template

apps_bp = Blueprint(
    "apps", __name__, url_prefix="/apps", template_folder="../templates"
)


@apps_bp.route("/")
def index():
    """Renders the main apps landing page."""
    apps_list = [
        {
            "name": "IOIT ACM Collage Maker",
            "description": "A simple tool to create collages from ACM Events, used for updating events on ACM INDIA Console.",
            "url": "apps.collage_maker",
            "icon": "image",
        }
    ]
    return render_template("apps/index.html", apps=apps_list)


@apps_bp.route("/collage-maker")
def collage_maker():
    """Renders the collage maker application page."""
    return render_template("apps/collage_maker.html")
