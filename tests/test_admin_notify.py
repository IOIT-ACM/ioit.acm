import unittest
from app import create_app, db
from app.models import User, Subscriber, EmailLog
from unittest.mock import patch


class AdminNotifyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create Admin User
        self.admin = User(
            name="Admin Test",
            username="admintest",
            branch="CS",
            mobile_no="1234567890",
            password="hashedpassword",
            is_admin=True,
        )
        # Create Normal User
        self.user = User(
            name="Normal User",
            username="normaluser",
            branch="IT",
            mobile_no="0987654321",
            password="hashedpassword",
            is_admin=False,
        )
        # Create Subscriber
        self.sub = Subscriber(email="sub@example.com", is_active=True)

        db.session.add_all([self.admin, self.user, self.sub])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, user):
        with self.client.session_transaction() as sess:
            sess["_user_id"] = str(user.id)

    @patch("app.blueprints.admin.mail.send")
    def test_admin_broadcast_success_and_email_log(self, mock_send):
        self.login(self.admin)
        payload = {
            "subject": "Test Broadcast Subject",
            "template_used": "custom",
            "body_html": "<p>Hello Subscribers!</p>",
            "event_slugs": [],
        }

        res = self.client.post("/events/admin/notify", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])

        # Confirm mail.send was called
        mock_send.assert_called_once()

        # Confirm EmailLog record created
        log = EmailLog.query.filter_by(subject="Test Broadcast Subject").first()
        self.assertIsNotNone(log)
        self.assertEqual(log.sent_by_user_id, self.admin.id)
        self.assertEqual(log.recipient_count, 1)

    @patch("app.blueprints.admin.mail.send")
    def test_duplicate_send_guard_within_60_seconds(self, mock_send):
        self.login(self.admin)
        payload = {
            "subject": "Duplicate Test Subject",
            "template_used": "custom",
            "body_html": "<p>Duplicate Body Content</p>",
            "event_slugs": [],
        }

        # First Send
        res1 = self.client.post("/events/admin/notify", json=payload)
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(mock_send.call_count, 1)

        # Immediate Duplicate Send Attempt
        res2 = self.client.post("/events/admin/notify", json=payload)
        self.assertEqual(res2.status_code, 429)
        data2 = res2.get_json()
        self.assertFalse(data2["success"])
        self.assertIn("less than a minute ago", data2["error"])

        # Confirm mail.send was NOT called a second time
        self.assertEqual(mock_send.call_count, 1)

        # Confirm only 1 EmailLog exists
        logs = EmailLog.query.filter_by(subject="Duplicate Test Subject").all()
        self.assertEqual(len(logs), 1)


if __name__ == "__main__":
    unittest.main()
