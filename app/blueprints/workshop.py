from flask import Blueprint, request, render_template, redirect, flash, url_for
from app.db import db
from ..models import WorkshopRegistration
import os
import requests
import re
from app import mail
from flask_mail import Message

workshop_bp = Blueprint("workshop", __name__, template_folder="../../templates/forms")

WORKSHOP_FORM_API_URL = os.getenv("WORKSHOP_FORM_API_URL")
WORKSHOP_FORM_API_KEY = os.getenv("WORKSHOP_FORM_API_KEY")


def str_to_bool(val):
    return val.strip().lower() in ["yes", "true", "1"]


def is_valid_email(email):
    return re.match(r"^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$", email)


def is_valid_mobile(mobile):
    return re.match(r"^\d{10}$", mobile)


@workshop_bp.route("/workshop", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.form

        required_fields = [
            "fullName", "email", "contactNumber", "collegeRoll",
            "yearOfStudy", "branch", "web3Familiar", "suiNetwork",
            "programmingLanguages", "agreement"
        ]

        missing = [f for f in required_fields if not data.get(f)]
        if missing:
            flash("Please fill out all required fields.", "danger")
            return redirect(url_for("workshop.register"))

        if not is_valid_email(data["email"]):
            flash("Invalid email format.", "danger")
            return redirect(url_for("workshop.register"))

        if not is_valid_mobile(data["contactNumber"]):
            flash("Invalid contact number format. Must be 10 digits.", "danger")
            return redirect(url_for("workshop.register"))

        try:
            entry = WorkshopRegistration(
                full_name=data["fullName"],
                email=data["email"],
                mobile=data["contactNumber"],
                college_roll=data["collegeRoll"],
                year_of_study=data["yearOfStudy"],
                branch=data["branch"],
                web3_familiar=str_to_bool(data["web3Familiar"]),
                sui_network=str_to_bool(data["suiNetwork"]),
                programming_languages=data["programmingLanguages"],
                portfolio=data.get("portfolio") or None
            )
            db.session.add(entry)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error_message = str(e)
            print("DB Error: {0}".format(error_message))

            try:
                msg = Message(
                    subject="IOIT ACM: Workshop Registration DB Error",
                    recipients=[os.getenv("WEBMASTER_EMAIL")],
                    body=(
                        "An error occurred during a workshop registration attempt.\n\n"
                        "Error Details:\n{0}\n\n"
                        "Form Data:\n"
                        "Full Name: {1}\n"
                        "Email: {2}\n"
                        "Contact: {3}\n"
                        "College Roll: {4}\n"
                        "Year: {5}\n"
                        "Branch: {6}\n"
                        "Web3 Familiar: {7}\n"
                        "Sui Network: {8}\n"
                        "Languages: {9}\n"
                        "Portfolio: {10}\n"
                    ).format(
                        error_message,
                        data.get('fullName'),
                        data.get('email'),
                        data.get('contactNumber'),
                        data.get('collegeRoll'),
                        data.get('yearOfStudy'),
                        data.get('branch'),
                        data.get('web3Familiar'),
                        data.get('suiNetwork'),
                        data.get('programmingLanguages'),
                        data.get('portfolio')
                    )
                )
                mail.send(msg)
            except Exception as mail_error:
                print("Error sending mail: {0}".format(mail_error))

        if WORKSHOP_FORM_API_URL and WORKSHOP_FORM_API_KEY:
            try:
                headers = {"Authorization": "Bearer {0}".format(WORKSHOP_FORM_API_KEY)}
                payload = {
                    "data": [{
                        "Full Name": entry.full_name,
                        "Email": entry.email,
                        "Mobile": entry.mobile,
                        "College Roll": entry.college_roll,
                        "Year": entry.year_of_study,
                        "Branch": entry.branch,
                        "Web3 Familiar": str(entry.web3_familiar),
                        "Sui Network Familiar": str(entry.sui_network),
                        "Languages": entry.programming_languages,
                        "Portfolio": entry.portfolio or "",
                        "Timestamp": entry.registered_on.isoformat()
                    }]
                }
                requests.post(WORKSHOP_FORM_API_URL, json=payload, headers=headers)
            except Exception as e:
                print("SheetDB Sync Error: {0}".format(str(e)))

        flash("You have successfully registered for the Move Programming Workshop!", "success")
        return redirect(url_for("workshop.register"))

    return render_template("workshop.html")
