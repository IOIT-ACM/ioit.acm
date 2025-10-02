from flask import Blueprint, render_template, request, make_response, jsonify
import os
import requests
from datetime import datetime, timedelta

form_bp = Blueprint(
    "ioit_acm_forms",
    __name__,
    template_folder="../templates/tmp",
)


@form_bp.route("/web3-interest-form", methods=["GET", "POST"])
def web3_interest_form():
    if request.method == "POST":
        origin = request.headers.get("Origin")

        allowed_origins = ["https://ioit.acm.org"]
        is_allowed = False

        if origin:
            if origin in allowed_origins:
                is_allowed = True

        if not is_allowed:
            return make_response(
                jsonify({"error": "Access from this origin is not allowed"}), 403
            )

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "No data received"}), 400)

        API_URL = os.getenv("WEB3_FORM_API_URL")
        BEARER_TOKEN = os.getenv("WEB3_FORM_BEARER_TOKEN")

        if not API_URL or not BEARER_TOKEN:
            return make_response(
                jsonify({"error": "Server is not configured to handle this request."}),
                500,
            )

        utc_now = datetime.utcnow()
        ist_now = utc_now + timedelta(hours=5, minutes=30)
        data["timestamp"] = ist_now.strftime("%Y-%m-%d %H:%M:%S")

        headers = {
            "Authorization": "Bearer {}".format(BEARER_TOKEN),
            "Content-Type": "application/json",
        }

        try:
            sheetdb_response = requests.post(
                API_URL, json={"data": [data]}, headers=headers
            )
            sheetdb_response.raise_for_status()
            response = make_response(
                jsonify({"success": True, "message": "Data submitted successfully"}),
                200,
            )
        except requests.exceptions.RequestException as e:
            print("Error sending data to SheetDB: {}".format(e))
            response = make_response(
                jsonify(
                    {
                        "error": "Failed to send data to the external service",
                        "details": str(e),
                    }
                ),
                502,
            )

        response.headers["Access-Control-Allow-Origin"] = origin
        return response

    return render_template("tmp/web3_interest_form.html")


@form_bp.route("/cloud-interest-form", methods=["GET", "POST"])
def cloud_interest_form():
    if request.method == "POST":
        origin = request.headers.get("Origin")

        allowed_origins = ["https://ioit.acm.org"]
        is_allowed = False

        if origin:
            if origin in allowed_origins:
                is_allowed = True

        if not is_allowed:
            return make_response(
                jsonify({"error": "Access from this origin is not allowed"}), 403
            )

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "No data received"}), 400)

        API_URL = os.getenv("CLOUD_FORM_API_URL")
        BEARER_TOKEN = os.getenv("CLOUD_FORM_BEARER_TOKEN")

        if not API_URL or not BEARER_TOKEN:
            return make_response(
                jsonify({"error": "Server is not configured to handle this request."}),
                500,
            )

        utc_now = datetime.utcnow()
        ist_now = utc_now + timedelta(hours=5, minutes=30)
        data["timestamp"] = ist_now.strftime("%Y-%m-%d %H:%M:%S")

        headers = {
            "Authorization": "Bearer {}".format(BEARER_TOKEN),
            "Content-Type": "application/json",
        }

        try:
            sheetdb_response = requests.post(
                API_URL, json={"data": [data]}, headers=headers
            )
            sheetdb_response.raise_for_status()
            response = make_response(
                jsonify({"success": True, "message": "Data submitted successfully"}),
                200,
            )
        except requests.exceptions.RequestException as e:
            print("Error sending data to SheetDB: {}".format(e))
            response = make_response(
                jsonify(
                    {
                        "error": "Failed to send data to the external service",
                        "details": str(e),
                    }
                ),
                502,
            )

        response.headers["Access-Control-Allow-Origin"] = origin
        return response

    return render_template("tmp/cloud_interest_form.html")


@form_bp.route("/tenet-phase1", methods=["GET"])
def tenet_phase1():
    return render_template("tmp/closed_forms_tenet.html") # form closed
    if request.method == "POST":
        origin = request.headers.get("Origin")

        allowed_origins = ["https://ioit.acm.org"]

        if not origin or origin not in allowed_origins:
            return make_response(
                jsonify({"error": "Access from this origin is not allowed"}), 403
            )

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "No data received"}), 400)

        API_URL = os.getenv("TENET_FORM_API_URL")
        BEARER_TOKEN = os.getenv("TENET_FORM_BEARER_TOKEN")

        if not API_URL or not BEARER_TOKEN:
            return make_response(
                jsonify({"error": "Server is not configured to handle this request."}),
                500,
            )

        utc_now = datetime.utcnow()
        ist_now = utc_now + timedelta(hours=5, minutes=30)
        data["timestamp"] = ist_now.strftime("%Y-%m-%d %H:%M:%S")

        headers = {
            "Authorization": "Bearer {}".format(BEARER_TOKEN),
            "Content-Type": "application/json",
        }

        try:
            sheetdb_response = requests.post(
                API_URL, json={"data": [data]}, headers=headers
            )
            sheetdb_response.raise_for_status()

            response = make_response(
                jsonify({"success": True, "message": "Data submitted successfully"}),
                200,
            )
        except requests.exceptions.RequestException as e:
            response = make_response(
                jsonify(
                    {
                        "error": "Failed to send data to the external service",
                        "details": str(e),
                    }
                ),
                502,
            )

        response.headers["Access-Control-Allow-Origin"] = origin
        return response

    return render_template("tmp/tenet.recruitment.phase1.html")

@form_bp.route("/tenet-phase2", methods=["GET", "POST"])
def tenet_phase2():
    return render_template("tmp/closed_forms_tenet.html") # form closed
    if request.method == "POST":
        origin = request.headers.get("Origin")

        allowed_origins = ["https://ioit.acm.org"]

        if not origin or origin not in allowed_origins:
            return make_response(
                jsonify({"error": "Unrestricted"}), 403
            )

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "No data received"}), 400)

        API_URL = os.getenv("TENET_FORM_API_URL")
        BEARER_TOKEN = os.getenv("TENET_FORM_BEARER_TOKEN")

        if not API_URL or not BEARER_TOKEN:
            return make_response(
                jsonify({"error": "Server is not configured to handle this request."}),
                500,
            )

        utc_now = datetime.utcnow()
        ist_now = utc_now + timedelta(hours=5, minutes=30)
        data["timestamp"] = ist_now.strftime("%Y-%m-%d %H:%M:%S")

        headers = {
            "Authorization": "Bearer {}".format(BEARER_TOKEN),
            "Content-Type": "application/json",
        }

        try:
            sheetdb_response = requests.post(
                API_URL, json={"data": [data]}, headers=headers
            )
            sheetdb_response.raise_for_status()

            response = make_response(
                jsonify({"success": True, "message": "Data submitted successfully"}),
                200,
            )
        except requests.exceptions.RequestException as e:
            response = make_response(
                jsonify(
                    {
                        "error": "Failed to send data to the external service",
                        "details": str(e),
                    }
                ),
                502,
            )

        response.headers["Access-Control-Allow-Origin"] = origin
        return response

    return render_template("tmp/tenet.recruitment.phase2.html")

@form_bp.route("/tenet-phase3", methods=["GET", "POST"])
def tenet_phase3():
    return render_template("tmp/closed_forms_tenet.html") # form closed
    if request.method == "POST":
        origin = request.headers.get("Origin")

        allowed_origins = ["https://ioit.acm.org"]

        if not origin or origin not in allowed_origins:
            return make_response(
                jsonify({"error": "Unrestricted"}), 403
            )

        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "No data received"}), 400)

        API_URL = os.getenv("TENET_FORM_API_URL")
        BEARER_TOKEN = os.getenv("TENET_FORM_BEARER_TOKEN")

        if not API_URL or not BEARER_TOKEN:
            return make_response(
                jsonify({"error": "Server is not configured to handle this request."}),
                500,
            )

        utc_now = datetime.utcnow()
        ist_now = utc_now + timedelta(hours=5, minutes=30)
        data["timestamp"] = ist_now.strftime("%Y-%m-%d %H:%M:%S")

        headers = {
            "Authorization": "Bearer {}".format(BEARER_TOKEN),
            "Content-Type": "application/json",
        }

        try:
            sheetdb_response = requests.post(
                API_URL, json={"data": [data]}, headers=headers
            )
            sheetdb_response.raise_for_status()

            response = make_response(
                jsonify({"success": True, "message": "Data submitted successfully"}),
                200,
            )
        except requests.exceptions.RequestException as e:
            response = make_response(
                jsonify(
                    {
                        "error": "Failed to send data to the external service",
                        "details": str(e),
                    }
                ),
                502,
            )

        response.headers["Access-Control-Allow-Origin"] = origin
        return response

    return render_template("tmp/tenet.recruitment.phase3.html")
