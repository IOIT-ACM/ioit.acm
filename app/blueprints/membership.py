import requests, os
import time
import json
from flask import Blueprint, render_template

membership_bp = Blueprint("membership", __name__, template_folder="../templates")

# Access environment variables
API_URL = os.getenv("MEMBERSHIP_FORM_API_URL")
BEARER_TOKEN = os.getenv("MEMBERSHIP_FORM_BEARER_TOKEN")

# In-memory cache
cache = {"data": None, "timestamp": 0}
CACHE_EXPIRY = 30000
DATA_JSON_FILE = "snapshot.json"

school_participants = [
    {
        "name": "Chaitali Khachane",
        "imageurl": "chaitali.jpeg",
        "school": "ACM India Winter School 2023",
    },
    {
        "name": "Sadgi Pandey",
        "imageurl": "sadgi.jpeg",
        "school": "ACM India Winter School 2023",
    },
    {
        "name": "Anjali Shukla",
        "imageurl": "anjali-shukla.jpeg",
        "school": "ACM India Summer School 2023",
    },
    {
        "name": "Sana Naqvi",
        "imageurl": "sana-naqvi.jpeg",
        "school": "ACM India Summer School on Compilers for AI/ML Programs",
    },
    {
        "name": "Shravani Shewale",
        "imageurl": "shravani-shewale.jpeg",
        "school": "ACM India Summer School 2022",
    },
    {
        "name": "Yash Vyavhare",
        "imageurl": "yash-v.jpeg",
        "school": "ACM India Summer School 2022",
    },
    {
        "name": "Tanmayee Mali",
        "imageurl": "tanmayee-mali.jpeg",
        "school": "ACM India Winter School 2022",
    },
]


def fetch_membership_data():
    """Fetch membership data from API, cache it, or load from fallback JSON file."""
    if not API_URL or not isinstance(API_URL, str):
        raise ValueError("API_URL is not defined or is not a valid string.")

    if not BEARER_TOKEN or not isinstance(BEARER_TOKEN, str):
        raise ValueError("BEARER_TOKEN is not defined or is not a valid string.")

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

        if cache.get("data"):
            print("Returning cached data...")
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
    return render_template("membership.html", school_participants=school_participants)


@membership_bp.route("/membership/status")
def membership_status():
    """Renders the membership status page."""
    if cache["data"] is None or (time.time() - cache["timestamp"] > CACHE_EXPIRY):
        members = fetch_membership_data()
    else:
        members = cache["data"]

    # Sort members by full name
    members = sorted(
        members, key=lambda m: "{} {}".format(m["First Name"], m["Last Name"])
    )

    return render_template("membership_status.html", members=members)
