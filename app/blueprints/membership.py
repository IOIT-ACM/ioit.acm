import csv
import requests
import time
import os
from flask import Blueprint, render_template
from dotenv import load_dotenv

membership_bp = Blueprint("membership", __name__, template_folder="../templates")

load_dotenv()

# In-memory cache
cache = {"data": None, "timestamp": 0}
CACHE_EXPIRY = 300  # 5 minutes


school_participants = [
    {"name": "Sakshi Mane", "imageurl": "sakshi-mane.jpeg", "school": "ACM India Summer School 2025"},
    {"name": "Devang Gandhi", "imageurl": "devang.jpeg", "school": "ACM India Summer School 2025"},
    {"name": "Chaitali Khachane", "imageurl": "chaitali.jpeg", "school": "ACM India Winter School 2023"},
    {"name": "Sadgi Pandey", "imageurl": "sadgi.jpeg", "school": "ACM India Winter School 2023"},
    {"name": "Anjali Shukla", "imageurl": "anjali-shukla.jpeg", "school": "ACM India Summer School 2023"},
    {"name": "Sana Naqvi", "imageurl": "sana-naqvi.jpeg", "school": "ACM India Summer School on Compilers for AI/ML Programs"},
    {"name": "Shravani Shewale", "imageurl": "shravani-shewale.jpeg", "school": "ACM India Summer School 2022"},
    {"name": "Yash Vyavhare", "imageurl": "yash-v.jpeg", "school": "ACM India Summer School 2022"},
    {"name": "Tanmayee Mali", "imageurl": "tanmay-mali.jpeg", "school": "ACM India Winter School 2022"},
]


def fetch_membership_data():
    """Fetch membership data from Google Sheet with in-memory caching and header normalization."""
    if cache["data"] and (time.time() - cache["timestamp"] < CACHE_EXPIRY):
        return cache["data"]

    members = []

    SHEET_URL = os.environ.get("ACM_MEMBERSHIP_SHEET_URL")

    try:
        r = requests.get(SHEET_URL, timeout=10)
        r.raise_for_status()
        decoded = r.content.decode("utf-8")
        reader = csv.DictReader(decoded.splitlines())

        reader.fieldnames = [h.strip() for h in reader.fieldnames]

        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}
            members.append({
                "Membership ID": row.get("Membership ID", ""),
                "Full Name": row.get("Full Name", "").title(),
                "Expiration Date": row.get("Expiration Date", ""),
            })

        cache["data"] = members
        cache["timestamp"] = time.time()

        return members

    except requests.RequestException as e:
        print("Error fetching Google Sheet:", e)
        return cache.get("data", [])


@membership_bp.route("/membership")
def team():
    """Renders the static membership team page."""
    return render_template("membership.html", school_participants=school_participants)


@membership_bp.route("/membership/status")
def membership_status():
    """Renders the dynamic membership status page from Google Sheet."""
    members = fetch_membership_data()

    members = sorted(members, key=lambda m: m.get("Full Name", ""))

    return render_template("membership_status.html", members=members)
