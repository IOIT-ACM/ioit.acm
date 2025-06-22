from flask import Blueprint, render_template, request, jsonify

recruitment_bp = Blueprint("recruitment", __name__, template_folder="../templates/forms")

@recruitment_bp.route("/recruitment", methods=["GET"])
def acm_recruitment_form():
    return render_template("recruitment.html")

@recruitment_bp.route("/recruitment", methods=["POST"])
def handle_acm_recruitment():
    try:
        data = request.get_json()
        print("\nACM Recruitment Form Data:")
        for k, v in data.items():
            print("%s: %s" % (k, v))
        return jsonify({"message": "Form data received successfully"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Failed to process form"}), 500
