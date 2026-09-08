import unittest
import os
from flask_mail import Message
from app import create_app, mail


class FlaskMailConfigTestCase(unittest.TestCase):
    def setUp(self):
        os.environ["USE_SQLITE"] = "true"
        os.environ["MAIL_SUPPRESS_SEND"] = "True"
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["MAIL_SUPPRESS_SEND"] = True
        self.client = self.app.test_client()

    def test_mail_configuration_loaded(self):
        self.assertEqual(self.app.config["MAIL_SERVER"], os.getenv("MAIL_SERVER", "localhost"))
        self.assertEqual(self.app.config["MAIL_PORT"], int(os.getenv("MAIL_PORT", 1025)))
        self.assertEqual(self.app.config["MAIL_DEFAULT_SENDER"], os.getenv("MAIL_DEFAULT_SENDER", "events@ioit.acm.org"))

    def test_send_mail_outbox(self):
        with self.app.app_context():
            with mail.record_messages() as outbox:
                msg = Message(
                    subject="Test Notification",
                    recipients=["subscriber@example.com"],
                    body="This is a test email sent to verify Flask-Mail configuration.",
                )
                mail.send(msg)
                self.assertEqual(len(outbox), 1)
                self.assertEqual(outbox[0].subject, "Test Notification")
                self.assertIn("subscriber@example.com", outbox[0].recipients)


if __name__ == "__main__":
    unittest.main()
