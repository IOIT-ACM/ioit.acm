import urllib.parse

from flask import Blueprint, render_template

from app import events_store

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


@events_bp.route("/events/<string:event_slug>")
def event_detail(event_slug):
    # LiteSpeed hands the path to the app still percent-encoded, so decode it
    # here as well; harmless where it is already decoded, since no event name
    # contains a "%".
    event = events_store.find_by_name(urllib.parse.unquote(event_slug))
    if not event:
        return render_template(
            "event_detail_404.html", events=events_store.all_events()
        )
    return render_template(
        "event_detail.html",
        event=event,
        events=events_store.all_events(),
        event_slug=event_slug,
        eventname=event["name"],
        is_upcoming=events_store.is_upcoming(event),
    )


@events_bp.route("/events")
def home():
    return render_template(
        "events.html",
        events=events_store.all_events(),
        images=images,
        images_2=images_2,
    )


@events_bp.route("/events/subscribe", methods=["POST"])
def subscribe():
    import re

    from flask import flash, jsonify, redirect, request, url_for
    from sqlalchemy.exc import IntegrityError

    from app.db import db
    from app.models import Subscriber

    data = request.get_json(silent=True) if request.is_json else request.form
    if data is None:
        if request.is_json:
            return jsonify({"success": False, "error": "Invalid email address."}), 400
        flash("Invalid email address.", category="error")
        return redirect(url_for("events.home"))
    email = (data.get("email") or "").strip()

    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not email or not re.match(email_regex, email):
        if request.is_json:
            return jsonify({"success": False, "error": "Invalid email address."}), 400
        flash("Invalid email address.", category="error")
        return redirect(url_for("events.home"))

    subscriber = db.session.scalars(
        db.select(Subscriber).filter_by(email=email)
    ).first()
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
        try:
            db.session.commit()
            msg = "Successfully subscribed to event notifications!"
        except IntegrityError:
            db.session.rollback()
            msg = "You are already subscribed to event notifications."

    if request.is_json:
        return jsonify({"success": True, "message": msg})

    flash(msg, category="success")
    return redirect(url_for("events.home"))
