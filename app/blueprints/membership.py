import requests
import time
import json
from flask import Blueprint, render_template

membership_bp = Blueprint("membership", __name__, template_folder="../templates")

API_URL = "https://sheetdb.io/api/v1/vn9yo1yzudzoh"
BEARER_TOKEN = "3zwed407ppm56msmwv87jng9ir30dcfd9qyvjack"

# In-memory cache
cache = {"data": None, "timestamp": 0}
CACHE_EXPIRY = 30000
DATA_JSON_FILE = "snapshot.json"

def fetch_membership_data():
    """Fetch membership data from API, cache it, or load from fallback JSON file."""
    headers = {"Authorization": "Bearer " + BEARER_TOKEN}
    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        members = response.json()
        # Update the cache
        cache["data"] = members
        cache["timestamp"] = time.time()
        return members
    except requests.exceptions.RequestException as e:
        print("Error fetching data from API: {}".format(e))
        
        if cache["data"]:
            return cache["data"]

        try:
            with open(DATA_JSON_FILE, "r") as file:
                print("Loading data from fallback file...")
                fallback_data = json.load(file)
                return fallback_data
        except (FileNotFoundError, json.JSONDecodeError) as json_error:
            print("Error loading fallback data: {}".format(json_error))
            return []

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
    members = sorted(members, key=lambda m: "{} {}".format(m["First Name"], m["Last Name"]))

    return render_template("membership_status.html", members=members)
