# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from app.data.events import events

# Define the blueprint
home_bp = Blueprint("home", __name__, template_folder="../templates")

images = [
    "https://ioit.acm.org/tenet/mun/2024/1.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/2.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/3.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/4.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/5.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/6.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/7.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/8.jpeg",
]
images_2 = [
    "https://ioit.acm.org/tenet/mun/2024/9.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/10.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/11.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/12.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/13.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/14.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/15.jpeg",
    "https://ioit.acm.org/tenet/mun/2024/16.jpeg",
]


@home_bp.route("/")
def home():
    return render_template(
        "home.html", events=events[:6], images=images, images_2=images_2
    )
