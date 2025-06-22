from flask import Blueprint, render_template, request, jsonify
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load env variables
load_dotenv()

recruitment_bp = Blueprint("recruitment", __name__, template_folder="../templates/forms")

API_URL = os.getenv("RECRUITMENT_FORM_API_URL")
BEARER_TOKEN = os.getenv("RECRUITMENT_FORM_BEARER_TOKEN")

@recruitment_bp.route("/recruitment", methods=["GET"])
def acm_recruitment_form():
    return render_template("recruitment.html")

@recruitment_bp.route("/recruitment", methods=["POST"])
def handle_acm_recruitment():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        # Required fields
        required_fields = ["fullName", "branch", "year", "mobile", "roleType", "whyApply"]
        role_fields = {
            "chief": "chiefRole",
            "domainhead": "domainRole",
            "mun": "munRole",
            "volunteer": "volunteerArea"
        }

        missing = [f for f in required_fields if not data.get(f)]
        role_type = data.get("roleType")
        if role_type in role_fields and not data.get(role_fields[role_type]):
            missing.append(role_fields[role_type])

        if missing:
            return jsonify({"error": "Missing required fields: %s" % ', '.join(missing)}), 400

        # Add timestamp (IST)
        ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
        data["date"] = ist_now.strftime("%d %b %Y %H:%M")

        headers = {
            "Authorization": "Bearer %s" % BEARER_TOKEN,
            "Content-Type": "application/json"
        }

        if API_URL:
            try:
                response = requests.post(API_URL, json={"data": [data]}, headers=headers)
                response.raise_for_status()
            except requests.RequestException:
                return jsonify({"error": "Failed to send data to API"}), 500
        else:
            return jsonify({"error": "API_URL is not configured"}), 500

        return jsonify({"message": "Form submitted successfully"}), 200

    except Exception:
        return jsonify({"error": "Failed to process form"}), 500
