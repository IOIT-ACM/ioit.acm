import unittest
from app import create_app, db
from app.models import User
from app.utils import admin_required
from flask import Blueprint, Flask


class AdminRequiredTestCase(unittest.TestCase):
    def setUp(self):
        import os

        os.environ["USE_SQLITE"] = "true"
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False

        # Add a throwaway test route to verify admin_required decorator
        test_bp = Blueprint("test_admin", __name__)

        @test_bp.route("/test-admin-protected")
        @admin_required
        def admin_protected():
            return "Admin Access Granted", 200

        self.app.register_blueprint(test_bp)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            # Clean up existing test users if present
            User.query.filter(User.username.in_(["normaluser", "adminuser"])).delete()
            db.session.commit()

            # Create normal user
            self.normal_user = User(
                name="Normal User",
                username="normaluser",
                branch="CS",
                mobile_no="1234567890",
                password="hashedpassword",
                is_admin=False,
            )
            # Create admin user
            self.admin_user = User(
                name="Admin User",
                username="adminuser",
                branch="CS",
                mobile_no="1234567890",
                password="hashedpassword",
                is_admin=True,
            )
            db.session.add(self.normal_user)
            db.session.add(self.admin_user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            User.query.filter(User.username.in_(["normaluser", "adminuser"])).delete()
            db.session.commit()

    def login(self, username, password="hashedpassword"):
        # Helper to log in user using test client session
        with self.client.session_transaction() as sess:
            with self.app.app_context():
                user = User.query.filter_by(username=username).first()
                sess["_user_id"] = str(user.id)

    def test_unauthenticated_access_returns_403(self):
        response = self.client.get("/test-admin-protected")
        self.assertEqual(response.status_code, 403)

    def test_non_admin_access_returns_403(self):
        self.login("normaluser")
        response = self.client.get("/test-admin-protected")
        self.assertEqual(response.status_code, 403)

    def test_admin_access_returns_200(self):
        self.login("adminuser")
        response = self.client.get("/test-admin-protected")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Admin Access Granted", response.data)


if __name__ == "__main__":
    unittest.main()
