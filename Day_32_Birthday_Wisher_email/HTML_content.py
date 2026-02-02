from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

sender = "abrsh067@gmail.com"
receiver = "natawase27@gmail.com"
password = "fwai mkro gomk bpyi"

msg = MIMEMultipart("alternative")
msg["Subject"] = "HTML Email Test"
msg["From"] = sender
msg["To"] = receiver

# Plain text + HTML version
text = "Hello, this is a plain text version."
html = """\
<html>
  <body>
    <h1 style="color:blue;">Hello from Python!</h1>
    <p>This is an <b>HTML email</b>.</p>
  </body>
</html>
"""

msg.attach(MIMEText(text, "plain"))
msg.attach(MIMEText(html, "html"))

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    print("✅ HTML Email sent!")
