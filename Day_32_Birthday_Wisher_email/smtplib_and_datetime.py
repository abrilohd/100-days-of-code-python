# import smtplib
#
# my_email = "abrsh067@gmail.com"
# password = "fwai mkro gomk bpyi"
#
# connection = smtplib.SMTP("smtp.gmail.com")
# connection.starttls()
# connection.login(user=my_email, password=password)
# connection.sendmail(
#     from_addr=my_email,
#     to_addrs="natawase27@gmail.com",
#     msg="Subject: hello natan Wase\n\nThis is the body of my email.  ")
# connection.close()
# print("✅ Email sent successfully!")

#### or ####

# with smtplib.SMTP("smtp.gmail.com") as connection:
#     connection.starttls()
#     connection.login(user=my_email, password=password)
#     connection.sendmail(
#         from_addr=my_email,
#         to_addrs="natawase27@gmail.com",
#         msg="Subject: hello natan Wase\n\nThis is the body of my email.  "
#     )


import datetime as dt

now = dt.datetime.now()
year = now.year
day = now.weekday()
month = now.month
print(day)

date_of_birth = dt.datetime(year=1995, month=12, day=16, hour=4)
print(date_of_birth)