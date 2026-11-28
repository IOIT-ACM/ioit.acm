"""Copy existing website accounts into the chapter's Clerk instance.

Each account whose username is an email is created in Clerk with that email and
its name, and with the existing password hash so members keep their password:

- Werkzeug `scrypt:` hashes are passed to Clerk as `scrypt_werkzeug`.
- Werkzeug `pbkdf2:sha256:<iterations>$salt$hex` hashes are converted to the
  Django `pbkdf2_sha256` format Clerk accepts.
- Anything else (for example legacy `sha256$` hashes) is created without a
  password; those members sign in with an email code or reset their password.

Accounts that already exist in Clerk (same email) are left alone, and usernames
that are not emails are reported, since Clerk needs an email.

The website takes admin access from Clerk organization roles, so with IDP_ORG
set (organization id or slug) current admins are given the `org:admin` role in
that organization, including admins who already had a Clerk account. The website then
matches people to their old row by email on their first Clerk sign-in, so their
history and admin rights carry over.

Dry run by default (reads the database, calls nothing that writes):

    CLERK_SECRET_KEY=sk_live_... uv run python scripts/migrate_users_to_clerk.py
    CLERK_SECRET_KEY=sk_live_... uv run python scripts/migrate_users_to_clerk.py --apply
"""

import argparse
import base64
import os
import re
import sys
import time

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from app.db import db  # noqa: E402
from app.models import User  # noqa: E402

CLERK_API = "https://api.clerk.com/v1"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PBKDF2_RE = re.compile(r"^pbkdf2:sha256:(\d+)\$([^$]+)\$([0-9a-f]+)$")


def clerk_password(stored_hash):
    """Return (digest, hasher) Clerk can import, or (None, None)."""
    if stored_hash.startswith("scrypt:"):
        return stored_hash, "scrypt_werkzeug"
    match = PBKDF2_RE.match(stored_hash)
    if match:
        iterations, salt, hex_hash = match.groups()
        digest = base64.b64encode(bytes.fromhex(hex_hash)).decode()
        return f"pbkdf2_sha256${iterations}${salt}${digest}", "pbkdf2_sha256"
    return None, None


def split_name(name):
    first, _, last = (name or "").strip().partition(" ")
    return first or None, last.strip() or None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--apply", action="store_true", help="create the accounts in Clerk"
    )
    args = parser.parse_args()

    secret = os.environ.get("CLERK_SECRET_KEY")
    if not secret:
        sys.exit("Set CLERK_SECRET_KEY (Clerk dashboard, API keys, Secret keys).")
    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {secret}"

    def clerk_user_id(email):
        resp = session.get(
            f"{CLERK_API}/users", params={"email_address": email}, timeout=20
        )
        resp.raise_for_status()
        found = resp.json()
        return found[0]["id"] if found else None

    org_id = None
    if os.environ.get("IDP_ORG"):
        resp = session.get(
            f"{CLERK_API}/organizations/{os.environ['IDP_ORG']}", timeout=20
        )
        resp.raise_for_status()
        org_id = resp.json()["id"]

    def make_admin(clerk_id):
        """Add the user to the organization as org:admin, or promote them."""
        body = {"user_id": clerk_id, "role": "org:admin"}
        url = f"{CLERK_API}/organizations/{org_id}/memberships"
        resp = session.post(url, json=body, timeout=20)
        if not resp.ok:
            resp = session.patch(
                f"{url}/{clerk_id}", json={"role": "org:admin"}, timeout=20
            )
        return resp

    app = create_app()
    with app.app_context():
        users = db.session.scalars(db.select(User).order_by(User.id)).all()

    stats = {
        "total": len(users),
        "exists": 0,
        "created": 0,
        "failed": 0,
        "admins": 0,
        "admins_granted": 0,
    }
    by_hasher = {"scrypt_werkzeug": 0, "pbkdf2_sha256": 0, "none": 0}
    not_email, failed = [], []
    seen = set()

    for user in users:
        email = user.username.strip().lower()
        if not EMAIL_RE.match(email):
            not_email.append(user.id)
            continue
        if email in seen:
            continue
        seen.add(email)

        grant_admin = bool(org_id and user.is_admin)
        stats["admins"] += grant_admin
        clerk_id = clerk_user_id(email)
        if clerk_id:
            stats["exists"] += 1
        else:
            digest, hasher = clerk_password(user.password or "")
            by_hasher[hasher or "none"] += 1
        if not args.apply:
            continue
        if clerk_id:
            if grant_admin:
                resp = make_admin(clerk_id)
                if resp.ok:
                    stats["admins_granted"] += 1
                else:
                    failed.append((user.id, resp.status_code, resp.text[:200]))
            continue

        first, last = split_name(user.name)
        body = {
            "email_address": [email],
            "first_name": first,
            "last_name": last,
            "external_id": str(user.id),
            "skip_password_checks": True,
        }
        if digest:
            body["password_digest"] = digest
            body["password_hasher"] = hasher
        else:
            body["skip_password_requirement"] = True
        resp = session.post(f"{CLERK_API}/users", json=body, timeout=20)
        if resp.ok:
            stats["created"] += 1
            if grant_admin:
                resp = make_admin(resp.json()["id"])
                if resp.ok:
                    stats["admins_granted"] += 1
                else:
                    failed.append((user.id, resp.status_code, resp.text[:200]))
        else:
            stats["failed"] += 1
            failed.append((user.id, resp.status_code, resp.text[:200]))
        time.sleep(0.1)  # stay well under Clerk's rate limits

    mode = "APPLIED" if args.apply else "DRY RUN (nothing created)"
    print(f"{mode}")
    print(f"  accounts in the website database: {stats['total']}")
    print(f"  already in Clerk:                 {stats['exists']}")
    print(
        f"  to create, keeping the password:  {by_hasher['scrypt_werkzeug'] + by_hasher['pbkdf2_sha256']}"
    )
    print(f"  to create, without a password:    {by_hasher['none']}")
    print(f"  skipped, username is not an email: {len(not_email)} (ids: {not_email})")
    if org_id:
        print(f"  admins to give org:admin:         {stats['admins']}")
    else:
        print("  IDP_ORG not set: admins will not get a Clerk role")
    if args.apply:
        print(f"  created: {stats['created']}, failed: {stats['failed']}")
        print(f"  admin roles granted: {stats['admins_granted']}")
        for user_id, status, text in failed:
            print(f"    id {user_id}: HTTP {status} {text}")


if __name__ == "__main__":
    main()
