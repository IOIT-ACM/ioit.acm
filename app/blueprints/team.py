from flask import Blueprint, render_template, url_for, request
from app.data.teams import team_data

# Define the blueprint
team_bp = Blueprint("team", __name__, template_folder="../templates")


@team_bp.route("/team")
def team():
    years = sorted(team_data.keys(), reverse=True)  # Sort years in descending order
    latest_year = years[0]  # Get the latest year
    selected_team_data = team_data.get(latest_year, [])

    # Add URLs for static image paths
    for member in selected_team_data:
        member["image_url"] = url_for("static", filename="img/team/" + member["image"])

    return render_template(
        "team.html",
        years=years,
        latest_year=latest_year,
        selected_team_data=selected_team_data,
    )


@team_bp.route("/fetch-team")
def fetch_team():
    year = request.args.get("year", max(team_data.keys(), key=int))
    selected_team_data = team_data.get(year, [])

    # Add URLs for static image paths
    for member in selected_team_data:
        member["image_url"] = url_for("static", filename="img/team/" + member["image"])

    # Render team members in grid layout with consistent styles
    rendered_cards = ""
    for member in selected_team_data:
        rendered_cards += """
        <div class="flex flex-col md:mx-auto md:w-[400px] w-auto bg-white text-blue-600 rounded-lg overflow-hidden shadow-lg">
            <!-- Image Section -->
            <img src="{image_url}" alt="{name}" class="w-full md:h-64 h-40 object-cover">
            <!-- Text Section -->
            <div class="p-3 md:p-4 w-full text-left">
                <h3 class="text-sm md:text-2xl font-semibold">{name}</h3>
                <p class="text-xs md:text-lg text-gray-400">{title}</p>
                <div class="flex gap-2 mt-2">
                    {github_link}
                    {linkedin_link}
                </div>
            </div>
        </div>
        """.format(
            image_url=member["image_url"],
            name=member["name"],
            title=member["title"],
            github_link=(
                '<a href="{url}" target="_blank" class="text-gray-500 hover:text-gray-300 transition duration-200"><i class="fab fa-github text-sm md:text-base"></i></a>'.format(
                    url=member["github"]
                )
                if member.get("github")
                else ""
            ),
            linkedin_link=(
                '<a href="{url}" target="_blank" class="text-blue-500 hover:text-blue-300 transition duration-200"><i class="fab fa-linkedin text-sm md:text-base"></i></a>'.format(
                    url=member["linkedin"]
                )
                if member.get("linkedin")
                else ""
            ),
        )

    # Return the rendered HTML as a response
    return rendered_cards
