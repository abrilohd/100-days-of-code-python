from twilio.rest import Client

account_sid = "AC08094a6199957c58cd393a409ed5cad2"
auth_token = "1c88b246a2435ce16791c632a6eb0ace"
client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Test message from Python Twilio 🚀",
    from_="+15076195903",      # Your Twilio number
    to="+251905747674"         # Your verified phone number
)

print(message.sid)