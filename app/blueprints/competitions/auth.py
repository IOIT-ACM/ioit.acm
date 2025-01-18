from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app.db import db

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("auth.profile"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("auth.profile"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash(
                "Username does not exist. Sign up to create a new account.",
                category="error",
            )

    return render_template("competitions/login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("auth.profile"))

    if request.method == "POST":
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        username = request.form.get("username")
        branch = request.form.get("branch")
        acm_id = request.form.get("acmId")
        mobile_no = request.form.get("mobileNo")
        password1 = request.form.get("password1")
        confirm_password = request.form.get("confirmPassword")

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", category="error")
            return render_template("competitions/signup.html")
        if password1 != confirm_password:
            flash("Passwords do not match.", category="error")
            return render_template("competitions/signup.html")
        if len(password1) < 8:
            flash("Password must be at least 8 characters long.", category="error")
            return render_template("competitions/signup.html")

        hashed_password = generate_password_hash(password1, method="sha256")

        full_name = "{} {}".format(first_name, last_name)

        new_user = User(
            name=full_name,
            username=username,
            branch=branch,
            acm_id=acm_id or None,
            mobile_no=mobile_no,
            password=hashed_password,
        )
        db.session.add(new_user)
        db.session.commit()

        flash(
            "Account created successfully for {}!".format(full_name), category="success"
        )
        return redirect(url_for("auth.signin"))

    return render_template("competitions/signup.html")


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
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while updating your profile.", category="error")

    return redirect(url_for("auth.profile"))


@auth_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")

    if not current_password or not new_password:
        flash("Both fields are required.", category="error")
        return redirect(url_for("auth.profile"))

    if not check_password_hash(current_user.password, current_password):
        flash("Current password is incorrect.", category="error")
        return redirect(url_for("auth.profile"))

    if len(new_password) < 8:
        flash("New password must be at least 8 characters long.", category="error")
        return redirect(url_for("auth.profile"))

    try:
        current_user.password = generate_password_hash(new_password, method="sha256")
        db.session.commit()

        flash("Password updated successfully!", category="success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while updating your password.", category="error")

    return redirect(url_for("auth.profile"))


@auth_bp.route("/delete_profile", methods=["POST"])
@login_required
def delete_profile():
    delete_password = request.form.get("delete_password")
    delete_confirmation = request.form.get("delete_confirmation")

    if not delete_password or not delete_confirmation:
        flash("Both fields are required.", category="error")
        return redirect(url_for("auth.profile"))

    if not check_password_hash(current_user.password, delete_password):
        flash("Password is incorrect.", category="error")
        return redirect(url_for("auth.profile"))

    if delete_confirmation != "rm -rf {}".format(current_user.username):
        flash("Confirmation text is incorrect.", category="error")
        return redirect(url_for("auth.profile"))

    try:
        db.session.delete(current_user)
        db.session.commit()
        flash("Profile deleted successfully.", category="success")
        return redirect(url_for("auth.signin"))
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting your profile.", category="error")
        return redirect(url_for("auth.profile"))
