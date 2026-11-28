"""Admin pages for adding, editing and deleting events (/events/admin/manage)."""

import os
import uuid
from datetime import date

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import login_required
from sqlalchemy.exc import IntegrityError

from app import events_store, limiter
from app.blueprints.admin import (
    ALLOWED_IMAGE_EXTENSIONS,
    MAX_IMAGE_SIZE,
    sniff_image_extension,
)
from app.db import db
from app.models import Event
from app.utils import admin_required, check_csrf

admin_events_bp = Blueprint("admin_events", __name__, template_folder="../templates")

UPLOAD_SUBDIR = os.path.join("uploads", "events")
URL_FIELDS = ("moredetails", "registration_link", "instagram_link", "facebook_link")


class FormError(ValueError):
    pass


def parse_day(value, label, required):
    value = (value or "").strip()
    if not value:
        if required:
            raise FormError(f"{label} is required.")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise FormError(f"{label} is not a valid date.") from None


def clean_url(value, label):
    value = (value or "").strip()
    if value and not value.startswith(("https://", "http://", "/")):
        raise FormError(f"{label} must be a full link starting with https://.")
    return value


def save_image(file):
    """Stores an uploaded image under static/uploads/events and returns its
    path. Raises FormError for anything that is not a real, small image."""
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise FormError("Unsupported image type. Use PNG, JPG, GIF or WEBP.")
    detected = sniff_image_extension(file.stream.read(16))
    if detected is None:
        raise FormError("That file does not look like a valid image.")
    file.stream.seek(0, os.SEEK_END)
    size = file.stream.tell()
    file.stream.seek(0)
    if size == 0:
        raise FormError("The uploaded image is empty.")
    if size > MAX_IMAGE_SIZE:
        raise FormError("Image is too large. Maximum size is 5 MB.")
    folder = os.path.join(current_app.root_path, "static", UPLOAD_SUBDIR)
    os.makedirs(folder, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{detected}"
    file.save(os.path.join(folder, filename))
    return url_for("static", filename=f"uploads/events/{filename}")


def apply_form(event, form, files):
    """Copies the submitted form onto `event`, raising FormError on bad input."""
    name = " ".join((form.get("name") or "").split())
    if not name:
        raise FormError("Name is required.")
    if "/" in name:
        raise FormError("The name cannot contain a slash, it is used in the page link.")
    if len(name) > 255:
        raise FormError("Name is too long.")
    start = parse_day(form.get("start_date"), "Start date", required=True)
    end = parse_day(form.get("end_date"), "End date", required=False)
    if end and end < start:
        raise FormError("End date cannot be before the start date.")

    image_url = clean_url(form.get("image_url"), "Image link")
    links = {
        field: clean_url(form.get(field), field.replace("_", " ").capitalize())
        for field in URL_FIELDS
    }
    # Saved last, so a mistake elsewhere in the form never leaves a stray file.
    upload = files.get("image")
    if upload and upload.filename:
        image_url = save_image(upload)

    event.name = name
    event.start_date = start
    event.end_date = end if end and end != start else None
    event.description = (form.get("description") or "").strip()
    event.image_url = image_url
    for field, value in links.items():
        setattr(event, field, value)
    event.topics_text = "\n".join(
        line.strip() for line in (form.get("topics") or "").splitlines() if line.strip()
    )


@admin_events_bp.route("/events/admin/manage")
@login_required
@admin_required
def list_events():
    return render_template("admin/events_list.html", events=events_store.all_events())


@admin_events_bp.route("/events/admin/manage/new", methods=["GET", "POST"])
@login_required
@admin_required
@limiter.limit("60 per minute", methods=["POST"])
def new_event():
    event = Event()
    if request.method == "POST":
        check_csrf()
        try:
            apply_form(event, request.form, request.files)
            db.session.add(event)
            db.session.commit()
        except FormError as e:
            db.session.rollback()
            flash(str(e), category="error")
        except IntegrityError:
            db.session.rollback()
            flash("An event with that name already exists.", category="error")
        else:
            flash(f"Added {event.name}.", category="success")
            return redirect(url_for("admin_events.list_events"))
    return render_template("admin/event_form.html", event=event, form=request.form)


@admin_events_bp.route("/events/admin/manage/<int:event_id>", methods=["GET", "POST"])
@login_required
@admin_required
@limiter.limit("60 per minute", methods=["POST"])
def edit_event(event_id):
    event = db.get_or_404(Event, event_id)
    if request.method == "POST":
        check_csrf()
        try:
            apply_form(event, request.form, request.files)
            db.session.commit()
        except FormError as e:
            db.session.rollback()
            flash(str(e), category="error")
        except IntegrityError:
            db.session.rollback()
            flash("An event with that name already exists.", category="error")
        else:
            flash(f"Saved {event.name}.", category="success")
            return redirect(url_for("admin_events.list_events"))
    return render_template("admin/event_form.html", event=event, form=request.form)


@admin_events_bp.route("/events/admin/manage/<int:event_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_event(event_id):
    check_csrf()
    event = db.get_or_404(Event, event_id)
    name = event.name
    db.session.delete(event)
    db.session.commit()
    flash(f"Deleted {name}.", category="success")
    return redirect(url_for("admin_events.list_events"))
