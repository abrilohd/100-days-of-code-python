# notification_manager.py
from twilio.rest import Client
from config.settings import TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_VIRTUAL_NUMBER, TWILIO_VERIFIED_NUMBER

class NotificationManager:
    def __init__(self):
        if not all([TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_VIRTUAL_NUMBER, TWILIO_VERIFIED_NUMBER]):
            print("[NotificationManager] Twilio not fully configured; SMS disabled.")
            self.client = None
        else:
            self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, message: str):
        if not self.client:
            print("[NotificationManager] SMS skipped (no Twilio client). Message:\n", message)
            return
        msg = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER
        )
        print(f"SMS sent, SID: {msg.sid}")
