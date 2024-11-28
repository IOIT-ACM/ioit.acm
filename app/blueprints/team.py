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

    # Render team members in a modern card layout
    rendered_cards = ""
    for member in selected_team_data:
        # Generate social media links
        social_links = ""

        if member.get("socials", {}).get("github"):
            social_links += """
            <a href="{github_url}" target="_blank"
                class="text-gray-600 hover:text-gray-400 transition duration-200">
                <i class="fab fa-github text-base"></i>
            </a>
            """.format(github_url=member["socials"]["github"])

        if member.get("socials", {}).get("linkedin"):
            social_links += """
            <a href="{linkedin_url}" target="_blank"
                class="text-blue-600 hover:text-blue-400 transition duration-200">
                <i class="fab fa-linkedin text-base"></i>
            </a>
            """.format(linkedin_url=member["socials"]["linkedin"])

        if member.get("socials", {}).get("instagram"):
            social_links += """
            <a href="{instagram_url}" target="_blank"
                class="text-pink-600 hover:text-pink-400 transition duration-200">
                <i class="fab fa-instagram text-base"></i>
            </a>
            """.format(instagram_url=member["socials"]["instagram"])

        if member.get("socials", {}).get("linktree"):
            social_links += """
            <a href="{linktree_url}" target="_blank"
                class="text-green-600 hover:text-green-400 transition duration-200">
                <i class="fas fa-link text-base"></i>
            </a>
            """.format(linktree_url=member["socials"]["linktree"])

        # Render member card
        rendered_cards += """
        <div
          class="flex flex-col items-center text-blue-600 rounded-lg overflow-hidden"
        >
          <!-- Image Section -->
          <div
            class="w-44 h-44 md:w-48 md:h-48 bg-gray-100 border border-gray-300 overflow-hidden rounded-full mb-4 shadow-lg"
          >
            <img
              src="{image_url}"
              alt="{name}"
              class="w-full h-full object-cover object-top transition-transform duration-300 hover:scale-110"
            />
          </div>
          <!-- Text Section -->
          <div class="p-4 text-center">
            <h3 class="text-lg font-semibold text-blue-800">{name}</h3>
            <p class="text-sm text-gray-500">{title}</p>
            <div class="flex justify-center gap-4 mt-3">
              {social_links}
            </div>
          </div>
        </div>
        """.format(
            image_url=url_for("static", filename="img/team/" + member["image"]),
            name=member["name"],
            title=member["title"],
            social_links=social_links,
        )

    # Return the rendered HTML as a response
    return rendered_cards
