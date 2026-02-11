import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()


# -------- Configuration --------
URL = "https://www.amazon.com/dp/B0FDX3XXV3"
TARGET_PRICE = 40  # dollars
MY_EMAIL = os.getenv("EMAIL_USER")
APP_PASSWORD = os.getenv("EMAIL_PASS")  # use app password (see notes below)
SMTP_SERVER = os.getenv("SMTP_SERVER")
PORT = int(os.getenv("SMTP_PORT"))
# --------------------------------

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

# Try to find price
price_tag = soup.select_one(".a-price-whole .a-price-fraction") or soup.find("span", class_="a-price-symbol")

if price_tag:
    price_text = price_tag.get_text().strip()
    price = float(price_text.replace("$", ""))
else:
    print("⚠️ Price not found — using mock value for testing.")
    price = 40.00  # fake value for testing email
    price_text = f"${price}"

# Find product title
title_tag = soup.find(id="productTitle")
title = title_tag.get_text().strip() if title_tag else "Unknown Product"

print(f"✅ Product: {title}\n💲 Current Price: {price_text}")

# --- Send Email if below target ---
if price < TARGET_PRICE:
    subject = "🔥 Price Alert: Your Amazon item is below target!"
    body = f"{title}\nCurrent price: {price_text}\nBuy now: {URL}"
    msg = f"Subject:{subject}\n\n{body}"

    with smtplib.SMTP(SMTP_SERVER, PORT) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=APP_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=msg.encode("utf-8")
        )
    print("📧 Email sent successfully!")
else:
    print("📈 Price still above target.")













# import requests
# from bs4 import BeautifulSoup
# import smtplib
#
# url = "https://www.amazon.com/Amazon-Essentials-Womens-Pointed-Charcoal/dp/B088K4SD5K/ref=sr_1_1_ffob_sspa?crid=27ZRRYW3NG0UV&dib=eyJ2IjoiMSJ9.aUOULtwiH4qJPGBrW5B1SSgvh8QKu4lOn4lrynRZeQTV29xGxkeqecuNlJ6Gt6VLKHcc058bSH79mBYJQ3HuGlUjEzEliTUZOX9oXxF5Ia3KlvvlgZgsnTdEioMBvC3aoUGJGWAQw3uNXpHaFuH3o4gIfwy00MMt2WJ-wtRhob9zEVlXJGVDUaHzgvbeeaZSNA-P0A4S0btiPZRypk3w_nJvJz2oOmCVyPRk17z0r4NIXiPq-jjUvlcW8ROYVaOaes4o8QzVFejizHpvF8PLzkXjfLOVqxNL8MEoNASXO-Q.44B90KSq3pUsJWoGqRYO2GTBw7GlJQ6L09El3SbRpqU&dib_tag=se&keywords=shoes&qid=1761723866&sprefix=shoe%2Caps%2C317&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1&psc=1"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9"
# }
#
# response = requests.get(url, headers=headers)
#
# print("Status:", response.status_code)
#
# soup = BeautifulSoup(response.text, "lxml")
#
# # Try multiple patterns Amazon uses for prices
# price_tag = soup.select_one(".a-price-whole.a-price-decimal") or soup.find("span", class_="a-price-whole")
#
# if price_tag:
#     price_text = price_tag.get_text().strip()
#     price_value = float(price_text.replace("$", ""))
#     print("✅ Current price:", price_value)
# else:
#     print("Price not found! Amazon likely blocked your request or changed the page structure.")
#
# # Optional: check what Amazon actually returned
# # print(soup.prettify()[:1000])
#
# price = 90.00
# BUY_PRICE = 100.00
#
# title = soup.find(id="productTitle").get_text().strip()
#
# if price < BUY_PRICE:
#     message = f"{title} is now {price}"
#
#
