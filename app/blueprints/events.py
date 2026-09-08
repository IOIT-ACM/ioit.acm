import urllib.parse
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
    return urllib.parse.quote(name)


def decode_slug(slug):
    return urllib.parse.unquote(slug)



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
        is_upcoming = event_date.date() >= datetime.now().date()
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


@events_bp.route("/events/subscribe", methods=["POST"])
def subscribe():
    import re
    from flask import request, jsonify, flash, redirect, url_for
    from app.db import db
    from app.models import Subscriber

    data = request.get_json(silent=True) if request.is_json else request.form
    email = (data.get("email") or "").strip()

    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not email or not re.match(email_regex, email):
        if request.is_json:
            return jsonify({"success": False, "error": "Invalid email address."}), 400
        flash("Invalid email address.", category="error")
        return redirect(url_for("events.home"))

    subscriber = Subscriber.query.filter_by(email=email).first()
    if subscriber:
        if not subscriber.is_active:
            subscriber.is_active = True
            db.session.commit()
            msg = "Welcome back! Your subscription has been reactivated."
        else:
            msg = "You are already subscribed to event notifications."
    else:
        new_sub = Subscriber(email=email, is_active=True)
        db.session.add(new_sub)
        db.session.commit()
        msg = "Successfully subscribed to event notifications!"

    if request.is_json:
        return jsonify({"success": True, "message": msg})

    flash(msg, category="success")
    return redirect(url_for("events.home"))

