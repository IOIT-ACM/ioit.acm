import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models import User


def set_admin(username, app=None):
    if app is None:
        app = create_app()

    with app.app_context():
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            print(f"Error: User with username '{username}' not found.")
            return False

        user.is_admin = True
        try:
            db.session.commit()
            print(f"Success: User '{username}' is now an admin.")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating user '{username}': {e}")
            return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/set_admin.py <username>")
        sys.exit(1)

    target_username = sys.argv[1]
    success = set_admin(target_username)
    sys.exit(0 if success else 1)
