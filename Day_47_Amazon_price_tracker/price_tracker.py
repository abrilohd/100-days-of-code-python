# price_tracker.py
from telnetlib import EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import smtplib
import time
import os
from dotenv import load_dotenv

load_dotenv()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# ---------------- Configuration ----------------
URL = "https://www.amazon.com/dp/B0FDX3XXV3?th=1&psc=1"
TARGET_PRICE = 40.0  # Set your target price here

YOUR_EMAIL = os.getenv("EMAIL_USER")
YOUR_PASSWORD = os.getenv("EMAIL_PASS")  # Use Gmail App Password
SMTP_ADDRESS = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))

CHECK_INTERVAL = 60 * 60  # check every 1 hour

# ---------------- Initialize WebDriver ----------------
service = Service("chromedriver.exe")  # Update path if needed
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # run in background
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 15)  # wait up to 15 seconds for elements


# ---------------- Functions ----------------
def get_price_and_title():
    driver.get(URL)

    try:
        # Wait until the price element loads
        price_element = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-offscreen"))
        )
        price_str = price_element.text.strip()
        if price_str:
            price = float(price_str.replace("$", "").replace(",", ""))
        else:
            price = None
    except Exception as e:
        print("Could not find price:", e)
        price = None

    try:
        title_element = driver.find_element(By.ID, "productTitle")
        title = title_element.text.strip()
    except Exception as e:
        print("Could not find title:", e)
        title = "Unknown Product"

    return price, title


def send_email(title, price):
    subject = "Amazon Price Alert!"
    body = f"{title} is now ${price}\nBuy it here: {URL}"
    msg = f"Subject:{subject}\n\n{body}"

    try:
        with smtplib.SMTP(SMTP_ADDRESS, SMTP_PORT) as connection:
            connection.starttls()
            connection.login(YOUR_EMAIL, YOUR_PASSWORD)
            connection.sendmail(
                from_addr=YOUR_EMAIL,
                to_addrs=YOUR_EMAIL,
                msg=msg.encode("utf-8")
            )
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)


def check_price():
    price, title = get_price_and_title()
    if price:
        print(f"{title} - Current Price: ${price}")
        if price < TARGET_PRICE:
            print("Price is below target! Sending email...")
            send_email(title, price)
        else:
            print("Price is still above target.")
    else:
        print("Price not found.")


# ---------------- Main Loop ----------------
if __name__ == "__main__":
    try:
        while True:
            check_price()
            print(f"Waiting {CHECK_INTERVAL / 60} minutes before next check...")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("Stopping price tracker...")
    finally:
        driver.quit()
