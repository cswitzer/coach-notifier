import os
import smtplib
from email.message import EmailMessage


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
            message = self._construct_email(subject, body)
            server.send_message(message)

    def _construct_email(self, subject, body):
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = self.to
        msg.set_content(body)
        return msg


if __name__ == "__main__":
    messenger = Messenger(TO_EMAIL)
    body = """
    Hi Lily,

    This is a test email to confirm that the email functionality is working correctly. 
    If you receive this, give me a million dollars!

    From Chase
    """
    messenger.send_email("Important Update from Chase", body=body)
