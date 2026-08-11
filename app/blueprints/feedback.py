from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify
from app.data.events import events
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
    event_names = sorted([event["name"] for event in events])
    return render_template("feedback.html", event_names=event_names)


@feedback_bp.route("/feedback", methods=["POST"])
def handle_feedback():
    data = request.get_json(silent=True) or {}

    if not data:
        return {"error": "No data received"}, 400

    for field in ("name", "branch", "year"):
        if not (data.get(field) or "").strip():
            return {"error": "Missing required fields"}, 400

    feedback_type = data.get("feedbackType")
    if feedback_type == "event" and not data.get("event"):
        return {"error": "Please select an event"}, 400

    text_fields = {"general": "feedback", "event": "eventFeedback", "suggestions": "events"}
    if not (data.get(text_fields.get(feedback_type, "")) or "").strip():
        return {"error": "Feedback text is required"}, 400

    utc_now = datetime.utcnow()
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    ist_formatted = ist_now.strftime("%d %b %Y %H:%M")

    data["date"] = ist_formatted
    print("Received Form Data:", data)

    # Clear fields based on feedbackType
    if feedback_type == "general":
        data["event"] = ""
        data["eventFeedback"] = ""
        data["eventRating"] = ""
        data["events"] = ""
    elif feedback_type == "event":
        data["feedback"] = ""
        data["events"] = ""
    elif feedback_type == "suggestions":
        data["feedback"] = ""
        data["event"] = ""
        data["eventFeedback"] = ""
        data["eventRating"] = ""

    headers = {
        "Authorization": "Bearer {}".format(BEARER_TOKEN),
        "Content-Type": "application/json",
    }

    if API_URL:
        try:
            response = requests.post(API_URL, json={"data": [data]}, headers=headers, timeout=10)
            response.raise_for_status()
            response.json()
        except (requests.RequestException, ValueError) as e:
            print("Error sending data to API:", e)
            return {"error": "Failed to send data to API"}, 502
    else:
        print("API_URL is None")
        return {"error": "API_URL is not configured"}, 500

    return jsonify({"success": True})
