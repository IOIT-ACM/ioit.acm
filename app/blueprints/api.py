from flask import Blueprint, jsonify, make_response, request
import os

api_bp = Blueprint("api", __name__, url_prefix="/api")


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
