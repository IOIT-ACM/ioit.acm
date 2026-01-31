from flask import Blueprint, render_template, request, jsonify
import requests
import os
import json
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

recruitment_bp = Blueprint(
    "recruitment", __name__, template_folder="../templates/forms"
)

API_URL = os.getenv("ACM_RECRUITMENT_FORM_API_URL")
BEARER_TOKEN = os.getenv("ACM_RECRUITMENT_FORM_BEARER_TOKEN")


def load_questions_config():
    try:
        config_path = os.path.join(
            os.path.dirname(__file__), "../data/forms/acm.25.json"
        )
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print("Error loading config: {}".format(e))
        return {}


@recruitment_bp.route("/recruitment", methods=["GET"])
def acm_recruitment_form():
    return render_template("closed.html")  # form closed


@recruitment_bp.route("/recruitment", methods=["POST"])
def handle_acm_recruitment():
    return (
        jsonify({"error": "This form is no longer accepting submissions."}),
        403,
    )  # form closed

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        required_fields = [
            "fullName",
            "branch",
            "year",
            "mobile",
            "roleType",
            "whyApply",
        ]
        questions_config = load_questions_config()

        role_specific_questions_map = {}
        for role, questions in questions_config.items():
            question_ids = [q["id"] for q in questions]
            role_specific_questions_map[role] = question_ids

        missing = [f for f in required_fields if not data.get(f)]
        rt = data.get("roleType")
        if rt and rt in role_specific_questions_map:
            for qf in role_specific_questions_map[rt]:
                if not data.get(qf):
                    missing.append(qf)

        if missing:
            return (
                jsonify(
                    {"error": "Missing required fields: {}".format(", ".join(missing))}
                ),
                400,
            )

        mobile_no = data.get("mobile")
        if not re.match(r"^[0-9]{10}$", mobile_no):
            return (
                jsonify({"error": "Please enter a valid 10-digit mobile number."}),
                400,
            )

        ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
        data["date"] = ist_now.isoformat()

        # Database saving logic has been removed here.

        headers = {
            "Authorization": "Bearer {}".format(BEARER_TOKEN),
            "Content-Type": "application/json",
        }

        if API_URL:
            try:
                resp = requests.post(API_URL, json={"data": [data]}, headers=headers)
                resp.raise_for_status()
                print("Posted data to external API successfully.")
            except requests.exceptions.RequestException as err:
                print("External API request failed: {}".format(err))
                return (
                    jsonify({"error": "External API error", "details": str(err)}),
                    500,
                )
        else:
            print("API_URL not configured. Skipping API sync.")

        return jsonify({"success": "Form submitted successfully"}), 200

    except Exception as e:
        print("Unhandled server error: {}".format(e))
        return jsonify({"error": "Server error", "details": str(e)}), 500
