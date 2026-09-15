import unittest
import os
import json
from app import create_app, db
from app.models import Subscriber

class EventsSubscribeTestCase(unittest.TestCase):
    def setUp(self):
        os.environ["USE_SQLITE"] = "true"
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            Subscriber.query.delete()
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            Subscriber.query.delete()
            db.session.commit()

    def test_subscribe_new_email_json(self):
        response = self.client.post(
            "/events/subscribe",
            data=json.dumps({"email": "test@example.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("Successfully subscribed", data["message"])

        with self.app.app_context():
            sub = Subscriber.query.filter_by(email="test@example.com").first()
            self.assertIsNotNone(sub)
            self.assertTrue(sub.is_active)

    def test_subscribe_existing_active_email_json(self):
        with self.app.app_context():
            db.session.add(Subscriber(email="existing@example.com", is_active=True))
            db.session.commit()

        response = self.client.post(
            "/events/subscribe",
            data=json.dumps({"email": "existing@example.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("already subscribed", data["message"])

        with self.app.app_context():
            subs = Subscriber.query.filter_by(email="existing@example.com").all()
            self.assertEqual(len(subs), 1)

    def test_subscribe_inactive_email_reactivates(self):
        with self.app.app_context():
            db.session.add(Subscriber(email="inactive@example.com", is_active=False))
            db.session.commit()

        response = self.client.post(
            "/events/subscribe",
            data=json.dumps({"email": "inactive@example.com"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("reactivated", data["message"])

        with self.app.app_context():
            sub = Subscriber.query.filter_by(email="inactive@example.com").first()
            self.assertTrue(sub.is_active)

    def test_subscribe_invalid_email(self):
        response = self.client.post(
            "/events/subscribe",
            data=json.dumps({"email": "invalid-email"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("Invalid email", data["error"])

if __name__ == "__main__":
    unittest.main()
