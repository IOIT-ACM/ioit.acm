from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_mail import Message
from app import mail
from app.db import db
from app.models import Subscriber, EmailLog
from app.utils import admin_required
from app.data.events import events

admin_bp = Blueprint("admin", __name__, template_folder="../templates")


@admin_bp.route("/events/admin/notify", methods=["GET"])
@login_required
@admin_required
def notify_dashboard():
    active_subscriber_count = Subscriber.query.filter_by(is_active=True).count()
    recent_logs = EmailLog.query.order_by(EmailLog.sent_at.desc()).limit(15).all()
    return render_template(
        "admin/notify.html",
        events=events,
        subscriber_count=active_subscriber_count,
        recent_logs=recent_logs,
    )


@admin_bp.route("/events/admin/notify", methods=["POST"])
@login_required
@admin_required
def send_notification():
    data = request.get_json(silent=True) if request.is_json else request.form

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

    # Server-side 60-second duplicate broadcast guard using EmailLog
    from datetime import datetime, timedelta
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
    recipient_emails = [sub.email for sub in active_subscribers]

    if not recipient_emails:
        if request.is_json:
            return jsonify({"success": False, "error": "No active subscribers found."}), 400
        flash("No active subscribers found.", category="error")
        return redirect(url_for("admin.notify_dashboard"))

    try:
        msg = Message(
            subject=subject,
            recipients=recipient_emails,
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

    if request.is_json:
        return jsonify({
            "success": True,
            "message": "Notification successfully sent to {} subscribers!".format(len(recipient_emails)),
            "log_id": email_log.id,
        })

    flash("Notification successfully sent to {} subscribers!".format(len(recipient_emails)), category="success")
    return redirect(url_for("admin.notify_dashboard"))
