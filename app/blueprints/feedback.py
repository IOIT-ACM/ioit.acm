from datetime import datetime, timedelta
from flask import Blueprint, render_template, request
import requests

feedback_bp = Blueprint("feedback", __name__, template_folder="../templates")

API_URL = "https://sheetdb.io/api/v1/tlw2smd5ckqs9"
BEARER_TOKEN = "ywztmb62pbcb3in37utjwr5un190k4e6u750y62q"


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

    response = requests.post(API_URL, json={"data": [data]}, headers=headers)

    print("API Response:", response.status_code, response.json())

    return render_template("feedback_popup.html")
