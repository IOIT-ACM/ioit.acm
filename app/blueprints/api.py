from flask import Blueprint, jsonify, make_response, request
from ..models import Recruitment
import os

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/recruitment/all", methods=["GET"])
def get_all_recruitment_data():
    origin = request.headers.get("Origin")

    allowed_origins = ["https://os.ioit.acm.org"]
    is_allowed = False

    if origin:
        if origin in allowed_origins:
            is_allowed = True
        elif "://localhost" in origin or "://127.0.0.1" in origin:
            is_allowed = True

    if not is_allowed:
        return make_response(
            jsonify({"error": "Access from this origin is not allowed"}), 403
        )

    try:
        submissions = Recruitment.query.all()
        data = []
        for submission in submissions:
            submission_data = {
                "id": submission.id,
                "fullName": submission.fullName,
                "branch": submission.branch,
                "year": submission.year,
                "mobile": submission.mobile,
                "roleType": submission.roleType,
                "experience": submission.experience,
                "whyApply": submission.whyApply,
                "date": submission.date.isoformat() if submission.date else None,
                "extra_answers": submission.extra_answers,
            }
            data.append(submission_data)

        response = make_response(jsonify(data))
        response.headers["Content-Type"] = "application/json"

    except Exception as e:
        print("Error fetching recruitment data: {}".format(e))
        response = make_response(
            jsonify({"error": "Server error", "details": str(e)}), 500
        )

    response.headers["Access-Control-Allow-Origin"] = origin

    return response


@api_bp.route("/formdata/<filename>", methods=["GET"])
def get_formdata_json(filename):
    # Only allow .json files and prevent directory traversal
    if not filename.endswith(".json") or "/" in filename or "\\" in filename:
        return make_response(jsonify({"error": "Invalid filename"}), 400)

    forms_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "forms"
    )
    file_path = os.path.join(forms_dir, filename)

    if not os.path.isfile(file_path):
        return make_response(jsonify({"error": "File not found"}), 404)

    try:
        with open(file_path, "r") as f:
            content = f.read()
        response = make_response(content)
        response.headers["Content-Type"] = "application/json"
        return response
    except Exception as e:
        return make_response(jsonify({"error": "Server error", "details": str(e)}), 500)
