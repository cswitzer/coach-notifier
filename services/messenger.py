from typing import Protocol
import smtplib
from email.message import EmailMessage
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
TEXTBELT_API_KEY = os.getenv("TEXTBELT_API_KEY")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
RECIPIENT_PHONE = os.getenv("RECIPIENT_PHONE")


# === Protocol ===
class Messenger(Protocol):
    def send_msg(self, message: str) -> None: ...


# === Email Messenger ===
class EmailMessenger:
    def __init__(self, to: str):
        self.to = to

    def send_msg(self, message: str) -> None:
        """e.g. of message:

        Alert: Test Message
        This is the body of the message.
        """
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            subject = self._extract_subject(message)
            email = self._construct_email(subject, message)
            server.send_message(email)

    def _extract_subject(self, message: str) -> str:
        # Use first line as subject, rest as body (if you want to split it like this)
        return message.splitlines()[0] if message else "No Subject"

    def _construct_email(self, subject: str, body: str) -> EmailMessage:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = self.to
        msg.set_content(body)
        return msg


# === SMS Messenger ===
class SMSMessenger:
    def __init__(self, to: str):
        self.to = to

    def send_msg(self, message: str) -> None:
        resp = requests.post(
            "https://textbelt.com/text",
            data={
                "phone": self.to,
                "message": message,
                "key": TEXTBELT_API_KEY,
            },
        )
        print(resp.json())


# === Usage ===
def notify(messenger: Messenger):
    message = "Hi, Honey!\nThis is the last test message."
    messenger.send_msg(message)


if __name__ == "__main__":
    # Change this to EmailMessenger or SMSMessenger
    messenger = SMSMessenger(RECIPIENT_PHONE)
    # messenger = EmailMessenger(RECIPIENT_EMAIL)
    # notify(messenger)
