import os
from datetime import datetime, timedelta
from flask_mail import Message
from app import mail

def get_ist_timestamp():
    utc_now = datetime.utcnow()
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    return ist_now.strftime("%d %b %Y %H:%M")

def alert(error_code, message):
    timestamp = get_ist_timestamp()

    subject = "[SERVER ALERT] %s Error Detected" % error_code
    body = (
        "An error occurred on the server.\n\n"
        "Error Code: {0}\n"
        "Message: {1}\n"
        "Timestamp (IST): {2}\n"
    ).format(error_code, message, timestamp)

    recipients = [
        os.getenv("WEBMASTER_EMAIL_PRIMARY"),
        os.getenv("WEBMASTER_EMAIL_SECONDARY")
    ]

    try:
        msg = Message(subject=subject, recipients=recipients, body=body)
        mail.send(msg)
    except Exception as e:
        print("Error sending alert email: {0}".format(e))
