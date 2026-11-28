from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from app.db import db

from ...models import User as Users

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signin")
def signin():
    """Accounts live in the chapter's Clerk instance; this page links there."""
    if current_user.is_authenticated:
        return redirect(url_for("auth.profile"))
    return render_template("competitions/login.html")


@auth_bp.route("/signup")
def signup():
    # New members create their account on Clerk's sign-up page.
    return redirect(url_for("clerk_auth.signup"))


@auth_bp.route("/signout")
@login_required
def signout():
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for("auth.signin"))


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("competitions/profile.html", user=current_user)


@auth_bp.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    name = request.form.get("name")
    branch = request.form.get("branch")
    acm_id = request.form.get("acm_id")
    mobile_no = request.form.get("mobile_no")

    if not name or not branch or not mobile_no:
        flash("All fields except ACM ID are required.", category="error")
        return redirect(url_for("auth.profile"))

    try:
        current_user.name = name
        current_user.branch = branch
        current_user.acm_id = acm_id
        current_user.mobile_no = mobile_no
        db.session.commit()

        flash("Profile updated successfully!", category="success")
    except Exception:
        db.session.rollback()
        flash("An error occurred while updating your profile.", category="error")

    return redirect(url_for("auth.profile"))


@auth_bp.route("/delete_profile", methods=["POST"])
@login_required
def delete_profile():
    delete_confirmation = request.form.get("delete_confirmation")

    if delete_confirmation != "rm -rf {}".format(current_user.username):
        flash("Confirmation text is incorrect.", category="error")
        return redirect(url_for("auth.profile"))

    try:
        db.session.delete(current_user)
        db.session.commit()
        flash("Profile deleted successfully.", category="success")
        return redirect(url_for("auth.signin"))
    except Exception:
        db.session.rollback()
        flash("An error occurred while deleting your profile.", category="error")
        return redirect(url_for("auth.profile"))


@auth_bp.route("/members")
def acm_users():
    members = db.session.scalars(db.select(Users).order_by(Users.name.desc())).all()
    user_branches = sorted(set(member.branch for member in members))
    return render_template(
        "members.html",
        members=members,
        user=current_user,
        user_branches=user_branches,
    )
