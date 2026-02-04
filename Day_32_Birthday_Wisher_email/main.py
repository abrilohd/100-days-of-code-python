import smtplib
import datetime as dt
import random

MY_EMAIL = "YourEmail@gmail.com"
MY_PASSWORD = "your google password"

now = dt.datetime.now()
weekday = now.weekday()
if weekday == 1:
    with open("quotes.txt") as quote_text:
        all_quote = quote_text.readlines()
        quote = random.choice(all_quote)
    print(quote)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg =f"Subject:Monday Motivation\n\n{quote}"
        )