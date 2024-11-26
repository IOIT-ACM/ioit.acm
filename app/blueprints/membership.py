import requests
import time
from flask import Blueprint, render_template

membership_bp = Blueprint("membership", __name__, template_folder="../templates")

API_URL = "https://sheetdb.io/api/v1/vn9yo1yzudzoh"
BEARER_TOKEN = "3zwed407ppm56msmwv87jng9ir30dcfd9qyvjack"

# In-memory cache
cache = {"data": None, "timestamp": 0}
CACHE_EXPIRY = 30000


def fetch_membership_data():
    """Fetch membership data from API and update cache."""
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        members = response.json()
        # Update the cache
        cache["data"] = members
        cache["timestamp"] = time.time()
        return members
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        # Return cached data if available, otherwise return an empty list
        return cache["data"] if cache["data"] else []


@membership_bp.route("/membership")
def team():
    """Renders the membership team page."""
    return render_template("membership.html")


@membership_bp.route("/membership/status")
def membership_status():
    """Renders the membership status page."""
    if cache["data"] is None or (time.time() - cache["timestamp"] > CACHE_EXPIRY):
        members = fetch_membership_data()
    else:
        members = cache["data"]

    # Sort members by full name
    members = sorted(members, key=lambda m: f"{m['First Name']} {m['Last Name']}")

    return render_template("membership_status.html", members=members)
