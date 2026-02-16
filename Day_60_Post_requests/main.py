from flask import Flask, render_template, request
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Environment Variables
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")

# Blog API Endpoint (Replace with your own if needed)
BLOG_API_URL = "https://api.npoint.io/c790b4d5cab58020d391"

# Fetch Posts Once (can later optimize with caching)
try:
    response = requests.get(BLOG_API_URL, timeout=5)
    response.raise_for_status()
    posts = response.json()
except Exception:
    posts = []


@app.route("/")
def home():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if not MY_EMAIL or not MY_PASSWORD:
            return render_template(
                "contact.html",
                msg_sent=False,
                error="Email configuration missing."
            )

        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        email_message = (
            f"Subject: New Contact Message\n\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n\n"
            f"Message:\n{message}"
        )

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(MY_EMAIL, MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg=email_message
                )
            return render_template("contact.html", msg_sent=True)

        except Exception:
            return render_template(
                "contact.html",
                msg_sent=False,
                error="Failed to send message."
            )

    return render_template("contact.html", msg_sent=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = next(
        (post for post in posts if post["id"] == index),
        None
    )
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
