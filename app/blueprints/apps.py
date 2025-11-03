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
            "description": "A simple tool to create collages from your favorite images. Perfect for event summaries and social media posts.",
            "url": "apps.collage_maker",
            "icon": "image",
        }
        # You can add more apps to this list in the future
    ]
    return render_template("apps/index.html", apps=apps_list)


@apps_bp.route("/collage-maker")
def collage_maker():
    """Renders the collage maker application page."""
    return render_template("apps/collage_maker.html")
