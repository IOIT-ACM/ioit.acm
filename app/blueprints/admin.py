# -*- coding: utf-8 -*-
import errno
import os
import re
import uuid
from datetime import datetime, timedelta
from flask import Blueprint, current_app, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_mail import Message
from app import mail, limiter
from app.db import db
from app.models import Subscriber, EmailLog
from app.utils import admin_required
from app.data.events import events

admin_bp = Blueprint("admin", __name__, template_folder="../templates")

FALLBACK_EVENT_IMAGE = "img/assets/acm.png"

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_EXTRA_RECIPIENTS = 100


def parse_extra_recipients(raw):
    """Parse a comma/newline separated string or list of one-off recipient
    emails for a single campaign. Returns (valid_emails, invalid_entries)."""
    if raw is None:
        items = []
    elif isinstance(raw, list):
        items = raw
    elif isinstance(raw, (str, bytes)) or hasattr(raw, "split"):
        items = re.split(r"[,\n]+", raw)
    else:
        items = []

    valid = []
    invalid = []
    seen = set()
    for item in items:
        email = (item or "").strip()
        if not email:
            continue
        key = email.lower()
        if key in seen:
            continue
        if EMAIL_RE.match(email):
            valid.append(email)
            seen.add(key)
        else:
            invalid.append(email)
    return valid, invalid


def abs_image_url(path):
    """Resolve an event's (possibly relative, possibly missing) image_url into an
    absolute URL, since email clients cannot resolve paths relative to the site."""
    if not path:
        return url_for("static", filename=FALLBACK_EVENT_IMAGE, _external=True)
    if path.startswith("http://") or path.startswith("https://"):
        return path
    relative = path.lstrip("/")
    if relative.startswith("static/"):
        relative = relative[len("static/"):]
    return url_for("static", filename=relative, _external=True)


def sniff_image_extension(head):
    """Identify an image's real format from its leading bytes, ignoring
    whatever extension the client claims."""
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if head.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if head.startswith(b"GIF87a") or head.startswith(b"GIF89a"):
        return "gif"
    if head[0:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    return None


@admin_bp.route("/events/admin/notify", methods=["GET"])
@login_required
@admin_required
@limiter.limit("60 per minute")
def notify_dashboard():
    active_subscriber_count = Subscriber.query.filter_by(is_active=True).count()
    recent_logs = EmailLog.query.order_by(EmailLog.sent_at.desc()).limit(15).all()
    return render_template(
        "admin/notify.html",
        subscriber_count=active_subscriber_count,
        recent_logs=recent_logs,
    )


@admin_bp.route("/events/admin/notify/events/search", methods=["GET"])
@login_required
@admin_required
@limiter.limit("120 per minute")
def search_notify_events():
    query = (request.args.get("q") or "").strip().lower()

    try:
        limit = int(request.args.get("limit", 15))
    except (TypeError, ValueError):
        limit = 15
    limit = max(1, min(limit, 50))

    try:
        offset = int(request.args.get("offset", 0))
    except (TypeError, ValueError):
        offset = 0
    offset = max(0, offset)

    if query:
        matches = [e for e in events if query in e["name"].lower()]
    else:
        matches = list(events)

    total = len(matches)
    page = matches[offset:offset + limit]

    results = [{
        "slug": e.get("slug"),
        "name": e["name"],
        "date": (e.get("date") or "").strip(),
        "image_url": abs_image_url(e.get("image_url")),
    } for e in page]

    return jsonify({
        "success": True,
        "results": results,
        "total": total,
        "has_more": offset + len(page) < total,
    })


@admin_bp.route("/events/admin/notify/subscribers/search", methods=["GET"])
@login_required
@admin_required
@limiter.limit("120 per minute")
def search_subscribers():
    query = (request.args.get("q") or "").strip()
    status = (request.args.get("status") or "all").strip().lower()

    try:
        limit = int(request.args.get("limit", 20))
    except (TypeError, ValueError):
        limit = 20
    limit = max(1, min(limit, 100))

    try:
        offset = int(request.args.get("offset", 0))
    except (TypeError, ValueError):
        offset = 0
    offset = max(0, offset)

    subscriber_query = Subscriber.query
    if status == "active":
        subscriber_query = subscriber_query.filter_by(is_active=True)
    elif status == "inactive":
        subscriber_query = subscriber_query.filter_by(is_active=False)
    if query:
        subscriber_query = subscriber_query.filter(Subscriber.email.ilike("%{}%".format(query)))

    total = subscriber_query.count()
    rows = subscriber_query.order_by(Subscriber.subscribed_at.desc()).offset(offset).limit(limit).all()

    results = [{
        "id": s.id,
        "email": s.email,
        "is_active": s.is_active,
        "subscribed_at": s.subscribed_at.strftime("%d %b %Y, %H:%M") if s.subscribed_at else None,
    } for s in rows]

    return jsonify({
        "success": True,
        "results": results,
        "total": total,
        "has_more": offset + len(rows) < total,
    })


@admin_bp.route("/events/admin/notify/upload-image", methods=["POST"])
@login_required
@admin_required
@limiter.limit("20 per minute")
def upload_notify_image():
    file = request.files.get("image")
    if file is None or file.filename == "":
        return jsonify({"success": False, "error": "No image file was provided."}), 400

    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({"success": False, "error": "Unsupported file type. Use PNG, JPG, GIF or WEBP."}), 400

    head = file.stream.read(16)
    file.stream.seek(0)
    detected = sniff_image_extension(head)
    if detected is None:
        return jsonify({"success": False, "error": "That file does not look like a valid image."}), 400

    file.stream.seek(0, os.SEEK_END)
    size = file.stream.tell()
    file.stream.seek(0)
    if size == 0:
        return jsonify({"success": False, "error": "The uploaded file is empty."}), 400
    if size > MAX_IMAGE_SIZE:
        return jsonify({"success": False, "error": "Image is too large. Maximum size is 5 MB."}), 400

    upload_dir = os.path.join(current_app.root_path, "static", "uploads", "notify")
    try:
        os.makedirs(upload_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    filename = "{}.{}".format(uuid.uuid4().hex, detected)
    file.save(os.path.join(upload_dir, filename))

    image_url = url_for("static", filename="uploads/notify/{}".format(filename), _external=True)
    return jsonify({"success": True, "url": image_url})


@admin_bp.route("/events/admin/notify/render", methods=["POST"])
@login_required
@admin_required
@limiter.limit("60 per minute")
def render_notification():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"success": False, "error": "Invalid or missing JSON body."}), 400

    mode = (data.get("mode") or "").strip()
    slugs = data.get("event_slugs") or []
    if not isinstance(slugs, list):
        slugs = [slugs]

    slug_set = set(slugs)
    selected = [e for e in events if e.get("slug") in slug_set]

    if mode == "single":
        if len(selected) != 1:
            return jsonify({"success": False, "error": "Select exactly one event for Single Event mode."}), 400
        event = selected[0]
        subject = "Upcoming ACM Event: {}".format(event["name"])
        body_html = render_template(
            "email/notification.html",
            mode="single",
            event=event,
            events=[],
            header_title="You're Invited!",
            header_desc="Join us for this upcoming event from AISSMS IOIT ACM.",
            abs_image_url=abs_image_url,
        )
    elif mode == "roundup":
        if not selected:
            return jsonify({"success": False, "error": "Select at least one event for Roundup mode."}), 400
        subject = " Don't Miss Out these upcoming ACM events!"
        body_html = render_template(
            "email/notification.html",
            mode="roundup",
            event=None,
            events=selected,
            header_title="Take a look at our upcoming events!",
            header_desc="Here's what's coming up from AISSMS IOIT ACM. Don't miss out!",
            abs_image_url=abs_image_url,
        )
    else:
        return jsonify({"success": False, "error": "Custom mode has no autofill template."}), 400

    return jsonify({"success": True, "subject": subject, "body_html": body_html})


@admin_bp.route("/events/admin/notify", methods=["POST"])
@login_required
@admin_required
@limiter.limit("20 per hour")
def send_notification():
    data = request.get_json(silent=True) if request.is_json else request.form
    if data is None:
        if request.is_json:
            return jsonify({"success": False, "error": "Invalid or missing JSON body."}), 400
        flash("Invalid or missing form data.", category="error")
        return redirect(url_for("admin.notify_dashboard"))

    subject = (data.get("subject") or "").strip()
    template_used = (data.get("template_used") or "custom").strip()
    body_html = (data.get("body_html") or "").strip()
    selected_slugs = data.getlist("event_slugs") if hasattr(data, "getlist") else data.get("event_slugs", [])

    if isinstance(selected_slugs, list):
        event_slugs_str = ",".join(selected_slugs)
    else:
        event_slugs_str = str(selected_slugs)

    if not subject or not body_html:
        if request.is_json:
            return jsonify({"success": False, "error": "Subject and body content are required."}), 400
        flash("Subject and body content are required.", category="error")
        return redirect(url_for("admin.notify_dashboard"))

    extra_emails, invalid_emails = parse_extra_recipients(data.get("extra_recipients"))
    if invalid_emails:
        error_msg = "These extra recipient addresses don't look valid: {}".format(", ".join(invalid_emails[:5]))
        if request.is_json:
            return jsonify({"success": False, "error": error_msg}), 400
        flash(error_msg, category="error")
        return redirect(url_for("admin.notify_dashboard"))
    if len(extra_emails) > MAX_EXTRA_RECIPIENTS:
        error_msg = "You can add at most {} extra recipients per campaign.".format(MAX_EXTRA_RECIPIENTS)
        if request.is_json:
            return jsonify({"success": False, "error": error_msg}), 400
        flash(error_msg, category="error")
        return redirect(url_for("admin.notify_dashboard"))

    # Server-side 60-second duplicate broadcast guard using EmailLog
    cutoff = datetime.utcnow() - timedelta(seconds=60)
    recent_duplicate = EmailLog.query.filter(
        EmailLog.subject == subject,
        EmailLog.body_snapshot == body_html,
        EmailLog.sent_at >= cutoff
    ).first()

    if recent_duplicate:
        error_msg = "A broadcast with this exact subject and content was sent less than a minute ago. Please wait before re-sending."
        if request.is_json:
            return jsonify({"success": False, "error": error_msg}), 429
        flash(error_msg, category="error")
        return redirect(url_for("admin.notify_dashboard"))

    active_subscribers = Subscriber.query.filter_by(is_active=True).all()
    subscriber_emails = [sub.email for sub in active_subscribers]
    seen_emails = {e.lower() for e in subscriber_emails}
    one_off_emails = [e for e in extra_emails if e.lower() not in seen_emails]
    recipient_emails = subscriber_emails + one_off_emails

    if not recipient_emails:
        if request.is_json:
            return jsonify({"success": False, "error": "No active subscribers or extra recipients to send to."}), 400
        flash("No active subscribers or extra recipients to send to.", category="error")
        return redirect(url_for("admin.notify_dashboard"))

    try:
        msg = Message(
            subject=subject,
            recipients=[current_app.config["MAIL_DEFAULT_SENDER"]],
            bcc=recipient_emails,
            html=body_html,
        )
        mail.send(msg)
    except Exception as e:
        if request.is_json:
            return jsonify({"success": False, "error": "Failed to send emails: {}".format(str(e))}), 500
        flash("Failed to send emails: {}".format(str(e)), category="error")
        return redirect(url_for("admin.notify_dashboard"))

    email_log = EmailLog(
        subject=subject,
        template_used=template_used,
        event_slugs=event_slugs_str,
        body_snapshot=body_html,
        sent_by_user_id=current_user.id,
        recipient_count=len(recipient_emails),
    )
    db.session.add(email_log)
    db.session.commit()

    success_message = "Notification successfully sent to {} recipient{}!".format(
        len(recipient_emails), "s" if len(recipient_emails) != 1 else ""
    )
    if one_off_emails:
        success_message += " ({} extra recipient{} included for this campaign.)".format(
            len(one_off_emails), "s" if len(one_off_emails) != 1 else ""
        )

    if request.is_json:
        return jsonify({
            "success": True,
            "message": success_message,
            "log_id": email_log.id,
        })

    flash(success_message, category="success")
    return redirect(url_for("admin.notify_dashboard"))
