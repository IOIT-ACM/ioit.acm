from flask import Blueprint, render_template, request, jsonify
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

recruitment_bp = Blueprint(
    "recruitment", __name__, template_folder="../templates/forms"
)

API_URL = os.getenv("ACM_RECRUITMENT_FORM_API_URL")
BEARER_TOKEN = os.getenv("ACM_RECRUITMENT_FORM_BEARER_TOKEN")


@recruitment_bp.route("/recruitment", methods=["GET"])
def acm_recruitment_form():
    return render_template("acm.recruitment.html")



# Table format:

# fullName,branch,year,mobile,roleType,experience,whyApply,date,ts_q1,ts_q2,ts_q3,mh_q1,mh_q2,mh_q3,wt_q1,wt_q2,wt_q3,dt_q1,dt_q2,dt_q3,tt_q1,tt_q2,tt_q3,em_q1,em_q2,em_q3,sig_web_technologies_q1,sig_web_technologies_q2,sig_web_technologies_q3,sig_web_technologies_github,sig_web_technologies_linkedin,sig_ai_ml_q1,sig_ai_ml_q2,sig_ai_ml_q3,sig_ai_ml_github,sig_ai_ml_linkedin,sig_mobile_dev_q1,sig_mobile_dev_q2,sig_mobile_dev_q3,sig_mobile_dev_github,sig_mobile_dev_linkedin,sig_cloud_devops_q1,sig_cloud_devops_q2,sig_cloud_devops_q3,sig_cloud_devops_github,sig_cloud_devops_linkedin


@recruitment_bp.route("/recruitment", methods=["POST"])
def handle_acm_recruitment():
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
            "experience",
            "whyApply",
        ]

        role_specific_questions_map = {
            "technical_secretary": ["ts_q1", "ts_q2", "ts_q3"],
            "media_head": ["mh_q1", "mh_q2", "mh_q3"],
            "web_team": ["wt_q1", "wt_q2", "wt_q3"],
            "doc_team": ["dt_q1", "dt_q2", "dt_q3"],
            "tech_team": ["tt_q1", "tt_q2", "tt_q3"],
            "event_management_team": ["em_q1", "em_q2", "em_q3"],
            "sig_web_technologies": [
                "sig_web_technologies_q1",
                "sig_web_technologies_q2",
                "sig_web_technologies_q3",
                "sig_web_technologies_github",
                "sig_web_technologies_linkedin",
            ],
            "sig_ai_ml": [
                "sig_ai_ml_q1",
                "sig_ai_ml_q2",
                "sig_ai_ml_q3",
                "sig_ai_ml_github",
                "sig_ai_ml_linkedin",
            ],
            "sig_mobile_dev": [
                "sig_mobile_dev_q1",
                "sig_mobile_dev_q2",
                "sig_mobile_dev_q3",
                "sig_mobile_dev_github",
                "sig_mobile_dev_linkedin",
            ],
            "sig_cloud_devops": [
                "sig_cloud_devops_q1",
                "sig_cloud_devops_q2",
                "sig_cloud_devops_q3",
                "sig_cloud_devops_github",
                "sig_cloud_devops_linkedin",
            ],
        }

        missing = [f for f in required_fields if not data.get(f)]

        rt = data.get("roleType")
        if rt and rt in role_specific_questions_map:
            for question_field in role_specific_questions_map[rt]:
                if not data.get(question_field):
                    missing.append(question_field)
        elif rt and rt not in role_specific_questions_map:
            pass

        if missing:
            return (
                jsonify({"error": "Missing required fields: %s" % ", ".join(missing)}),
                400,
            )

        ist_now = datetime.utcnow() + timedelta(hours=5, minutes=30)
        data["date"] = ist_now.strftime("%d %b %Y %H:%M")

        headers = {
            "Authorization": "Bearer %s" % BEARER_TOKEN,
            "Content-Type": "application/json",
        }

        if API_URL:
            try:
                resp = requests.post(API_URL, json={"data": [data]}, headers=headers)
                resp.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                return (
                    jsonify(
                        {
                            "error": "Failed to send data to API due to server error",
                            "details": str(http_err),
                        }
                    ),
                    resp.status_code if "resp" in locals() else 500,
                )
            except requests.exceptions.RequestException as req_err:
                return (
                    jsonify(
                        {
                            "error": "Failed to send data to API due to network issue",
                            "details": str(req_err),
                        }
                    ),
                    500,
                )
        else:
            print("API_URL not configured")

        return render_template("acm.form-submission.html"), 200

    except Exception as e:
        return (
            jsonify(
                {
                    "error": "Failed to process form due to an unexpected error",
                    "details": str(e),
                }
            ),
            500,
        )