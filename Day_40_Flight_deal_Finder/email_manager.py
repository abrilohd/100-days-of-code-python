import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import EMAIL_ADDRESS, EMAIL_PASSWORD

class EmailManager:
    def __init__(self):
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            print("[EmailManager] Email not fully configured; sending disabled.")
            self.enabled = False
        else:
            self.enabled = True
            self.sender = EMAIL_ADDRESS
            self.password = EMAIL_PASSWORD

    def send_email(self, subject: str, body: str, to_email: str):
        if not self.enabled:
            print("[EmailManager] Email skipped (not configured).", subject, to_email)
            return
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
