import os
import requests
import smtplib


from dotenv import load_dotenv


load_dotenv()


TO_EMAIL = os.getenv("RECIPIENT_EMAIL")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


class Messenger:
    def __init__(self, to: str):
        self.to = to

    def send_email(self, subject, body):
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(SMTP_USER, self.to, message)


if __name__ == "__main__":
    messenger = Messenger("chase@vssta.com")
    messenger.send_email("Coach Notifier Test", "Hi, Chase!")
