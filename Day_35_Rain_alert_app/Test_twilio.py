import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

message = client.messages.create(
    body=" Twilio test message from Python",
    from_=os.getenv("TWILIO_FROM_NUMBER"),
    to=os.getenv("TWILIO_TO_NUMBER")
)

print(message.sid)
