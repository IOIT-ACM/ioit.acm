import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models import User


def set_admin(username, grant=True, app=None):
    if app is None:
        app = create_app()

    with app.app_context():
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            print(f"Error: User with username '{username}' not found.")
            return False

        user.is_admin = grant
        status_str = "an admin" if grant else "no longer an admin"
        try:
            db.session.commit()
            print(f"Success: User '{username}' is now {status_str}.")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user '{username}': {e}")
            return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/set_admin.py <username> [--grant | --revoke]")
        sys.exit(1)

    target_username = sys.argv[1]
    grant_admin = True

    if len(sys.argv) >= 3:
        flag = sys.argv[2].lower()
        if flag in ("--revoke", "--remove", "revoke", "remove", "false"):
            grant_admin = False
        elif flag in ("--grant", "grant", "true"):
            grant_admin = True

    success = set_admin(target_username, grant=grant_admin)
    sys.exit(0 if success else 1)

