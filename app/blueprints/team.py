from flask import Blueprint, render_template, request, jsonify, abort
from app.data.teams import team_data

# Define the blueprint
team_bp = Blueprint("team", __name__, template_folder="../templates")


@team_bp.route("/team")
def team():
    years = sorted(team_data.keys(), reverse=True)
    latest_year = years[0]

    year = request.args.get("year", latest_year)

    if year not in team_data:
        year = latest_year

    selected_team_data = team_data.get(year, [])

    return render_template(
        "team.html",
        years=years,
        latest_year=latest_year,
        selected_team_data=selected_team_data,
    )


@team_bp.route("/fetch-team")
def fetch_team():
    year = request.args.get("year")
    if year not in team_data:
        return jsonify({"error": "Team data for year {} not found".format(year)}), 404

    return jsonify(team_data[year])


@team_bp.route("/team/<int:year>")
def get_team_by_year(year):
    year_str = str(year)
    if year_str not in team_data:
        abort(404, description="Team data for year {0} not found.".format(year_str))

    return jsonify(team_data[year_str])
