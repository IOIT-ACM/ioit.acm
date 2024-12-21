from datetime import datetime, timedelta
from flask import Blueprint, render_template, request
import requests, os
from dotenv import load_dotenv

feedback_bp = Blueprint("feedback", __name__, template_folder="../templates")

# Load environment variables from .env file
load_dotenv()

# Access environment variables
API_URL = os.getenv("FEEDBACK_FORM_API_URL")
BEARER_TOKEN = os.getenv("FEEDBACK_FORM_BEARER_TOKEN")


@feedback_bp.route("/feedback", methods=["GET"])
def feedback_form():
    return render_template("feedback.html")


@feedback_bp.route("/feedback", methods=["POST"])
def handle_feedback():
    data = request.form.to_dict()

    utc_now = datetime.utcnow()
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    ist_formatted = ist_now.strftime("%d %b %Y %H:%M")

    data["date"] = ist_formatted

    print("Received Form Data:", data)

    headers = {
        "Authorization": "Bearer {}".format(BEARER_TOKEN),
        "Content-Type": "application/json",
    }

    if API_URL:
        response = requests.post(API_URL, json={"data": [data]}, headers=headers)
    else:
        raise ValueError("API_URL cannot be None")

    print("API Response:", response.status_code, response.json())

    return render_template("feedback_popup.html")
