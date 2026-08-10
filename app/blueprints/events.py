import urllib
try:
    from urllib import quote, unquote
except ImportError:
    from urllib.parse import quote, unquote
from flask import Blueprint, render_template
from app.data.events import events

events_bp = Blueprint("events", __name__, template_folder="../templates")

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


def safe_slug(name):
    try:
        return quote(name.encode("utf-8"))
    except TypeError:
        return quote(name)


def decode_slug(slug):
    try:
        return unquote(slug).decode("utf-8")
    except (AttributeError, TypeError):
        return unquote(slug)


for event in events:
    event["slug"] = safe_slug(event["name"])


@events_bp.route("/events/<string:event_slug>")
def event_detail(event_slug):
    from datetime import datetime
    decoded_name = decode_slug(event_slug)
    event = next((e for e in events if e["name"] == decoded_name), None)
    eventname = event["name"] if event else None
    if not event:
        return render_template("event_detail_404.html", events=events)
    is_upcoming = False
    try:
        date_str = event["date"].strip()
        if " - " in date_str:
            date_str = date_str.split(" - ")[0].strip()
            if len(date_str.split()) == 2:
                year = event["date"].strip().split(",")[-1].strip()
                date_str = date_str + ", " + year
        event_date = datetime.strptime(date_str, "%B %d, %Y")
        is_upcoming = event_date > datetime.now()
    except ValueError:
        pass
    return render_template(
        "event_detail.html",
        event=event,
        events=events,
        event_slug=event_slug,
        eventname=eventname,
        is_upcoming=is_upcoming,
    )


@events_bp.route("/events")
def home():
    return render_template(
        "events.html", events=events, images=images, images_2=images_2
    )
