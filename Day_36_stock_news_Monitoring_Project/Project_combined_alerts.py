"""
combined_alerts.py
Combines:
 - Rain alert using OpenWeatherMap (forecast)
 - Stock news alert using AlphaVantage + NewsAPI
 - Sends SMS via Twilio for any alerts

Usage:
  1. Create a .env file (see .env.example) with your keys & phone numbers.
  2. pip install -r requirements.txt
  3. python combined_alerts.py
"""

import os
import time
import requests
from requests.exceptions import RequestException, Timeout
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("OWM_API_KEY")
# ------------------------
# CONFIG / ENV VARIABLES
# ------------------------
# OpenWeatherMap
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"  # 5 day / 3 hour forecast

# AlphaVantage & NewsAPI
STOCK_API_KEY = os.getenv("STOCK_API_KEY")      # AlphaVantage
NEWS_API_KEY = os.getenv("NEWS_API_KEY")        # NewsAPI
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Twilio
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
VIRTUAL_TWILIO_NUMBER = os.getenv("VIRTUAL_TWILIO_NUMBER")  # Twilio phone number e.g. +15017122661
VERIFIED_NUMBER = os.getenv("VERIFIED_NUMBER")              # Your phone (must be verified on trial)

# Application settings (change as desired)
LOCATION_LAT = float(os.getenv("LOCATION_LAT", "46.947975"))   # default example coordinates
LOCATION_LON = float(os.getenv("LOCATION_LON", "7.447447"))
RAIN_CHECK_HOURS = int(os.getenv("RAIN_CHECK_HOURS", "12"))    # check next N hours for rain
STOCK_SYMBOL = os.getenv("STOCK_SYMBOL", "TSLA")               # ticker to check
COMPANY_NAME = os.getenv("COMPANY_NAME", "Tesla Inc")          # used for news queries
STOCK_PERCENT_THRESHOLD = float(os.getenv("STOCK_PERCENT_THRESHOLD", "5"))  # percent threshold
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))      # seconds for HTTP requests
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))               # basic retry loop

# ------------------------
# HELPERS
# ------------------------
def safe_get(url, params=None, timeout=REQUEST_TIMEOUT, max_retries=MAX_RETRIES):
    """
    Simple GET with retries and timeout. Returns response.json() or raises.
    """
    last_exc = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp
        except Timeout as e:
            print(f"[WARN] Timeout on attempt {attempt}/{max_retries} for {url}")
            last_exc = e
            time.sleep(1)
        except RequestException as e:
            print(f"[WARN] Request exception on attempt {attempt}/{max_retries} for {url}: {e}")
            last_exc = e
            time.sleep(1)
    # after retries
    raise last_exc

def send_sms_via_twilio(body: str):
    """
    Send an SMS via Twilio. Returns message SID or raises exception.
    """
    if not all([TWILIO_SID, TWILIO_AUTH_TOKEN, VIRTUAL_TWILIO_NUMBER, VERIFIED_NUMBER]):
        raise RuntimeError("Twilio configuration is incomplete. Check .env")
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=VIRTUAL_TWILIO_NUMBER,
        to=VERIFIED_NUMBER

    )
    print(f"[INFO] Sent SMS (sid={message.sid})")
    return message.sid

# ------------------------
# RAIN ALERT (OpenWeatherMap)
# ------------------------
def check_rain_forecast(lat: float, lon: float, hours_ahead: int = RAIN_CHECK_HOURS):
    """
    Checks OpenWeatherMap 5-day/3-hour forecast for rain within the next `hours_ahead`.
    Returns a tuple (will_rain_bool, details_string)
    """

    params =  {
    "lat": 9.03,
    "lon": 38.74,
    "appid": api_key,
    "cnt": 4,
}
    try:
        resp = safe_get(OWM_ENDPOINT, params=params)
    except Exception as e:
        print(f"[ERROR] Could not fetch weather data: {e}")
        return False, f"Weather API error: {e}"

    data = resp.json()
    # 'list' contains forecasts in 3-hour intervals
    forecasts = data.get("list", [])
    if not forecasts:
        return False, "No forecast data returned."

    seconds_ahead = hours_ahead * 3600
    will_rain = False
    rain_entries = []

    current_time = int(time.time())
    for entry in forecasts:
        # entry['dt'] is unix timestamp; check horizon
        ts = entry.get("dt", 0)
        if ts - current_time > seconds_ahead:
            continue
        # OpenWeatherMap uses 'weather' list. Weather id or main string can say 'Rain'
        weather_list = entry.get("weather", [])
        main_texts = [w.get("main", "") for w in weather_list]
        # also check 'rain' key for predicted mm
        rain_info = entry.get("rain", {})
        if any("Rain" in s or "Drizzle" in s for s in main_texts) or rain_info:
            will_rain = True
            # build readable time
            dt_txt = entry.get("dt_txt", "")
            rain_entries.append({
                "time": dt_txt,
                "weather": main_texts,
                "rain_volume": rain_info.get("3h", rain_info.get("1h", 0))
            })

    if will_rain:
        details = f"Rain expected within next {hours_ahead} hours:\n"
        for e in rain_entries[:5]:
            details += f"- {e['time']} | weather={e['weather']} | rain_vol={e['rain_volume']}\n"
        return True, details
    else:
        return False, f"No rain forecast in the next {hours_ahead} hours."

# ------------------------
# STOCK NEWS ALERT (AlphaVantage + NewsAPI)
# ------------------------
def get_daily_time_series(symbol: str):
    """
    Returns the Time Series (Daily) dict from AlphaVantage or raises.
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": STOCK_API_KEY
    }
    try:
        resp = safe_get(STOCK_ENDPOINT, params=params)
    except Exception as e:
        raise RuntimeError(f"AlphaVantage request failed: {e}")

    parsed = resp.json()
    if "Time Series (Daily)" not in parsed:
        # AlphaVantage may return a note about rate limiting
        raise RuntimeError(f"Unexpected AlphaVantage response: {parsed.get('Note') or parsed}")
    return parsed["Time Series (Daily)"]

def analyze_stock_and_get_news(symbol: str, company_name: str, percent_threshold: float = STOCK_PERCENT_THRESHOLD):
    """
    Returns (should_alert_bool, formatted_articles_list or message_str)
    """
    try:
        ts = get_daily_time_series(symbol)
    except Exception as e:
        return False, f"Stock API error: {e}"

    # Convert dict to list sorted by date descending; keys are date strings in YYYY-MM-DD
    dates = sorted(ts.keys(), reverse=True)
    if len(dates) < 2:
        return False, "Not enough stock data to compare."

    yesterday = ts[dates[0]]
    day_before = ts[dates[1]]

    close_yesterday = float(yesterday["4. close"])
    close_day_before = float(day_before["4. close"])

    # percent change = (yesterday - day_before) / day_before * 100
    difference = close_yesterday - close_day_before
    diff_percent = (difference / close_day_before) * 100
    diff_percent_rounded = round(diff_percent, 2)
    arrow = "🔺" if diff_percent > 0 else "🔻"

    print(f"[INFO] {symbol} close yesterday: {close_yesterday}, day before: {close_day_before}, change: {diff_percent_rounded}%")

    if abs(diff_percent) >= percent_threshold:
        # fetch news
        news_params = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": company_name,
            "sortBy": "publishedAt",
            "pageSize": 3,
        }
        try:
            news_resp = safe_get(NEWS_ENDPOINT, params=news_params)
        except Exception as e:
            return True, [f"{symbol}: {arrow}{diff_percent_rounded}%\nNews API error: {e}"]

        articles = news_resp.json().get("articles", [])
        # Build formatted messages
        formatted = []
        if not articles:
            formatted.append(f"{symbol}: {arrow}{diff_percent_rounded}%\nNo news articles found for '{company_name}'.")
        else:
            for a in articles[:3]:
                title = a.get("title", "No title")
                desc = a.get("description") or ""
                url = a.get("url") or ""
                message = f"{symbol}: {arrow}{diff_percent_rounded}%\nHeadline: {title}\nBrief: {desc}\n{url}"
                formatted.append(message)
        return True, formatted
    else:
        return False, f"{symbol}: change {diff_percent_rounded}% is below threshold {percent_threshold}%."

# ------------------------
# MAIN: run both checks and send SMS if needed
# ------------------------
def main():
    alerts_sent = 0
    # 1) Rain check
    print("[STEP] Checking weather for rain...")
    try:
        rain_bool, rain_details = check_rain_forecast(LOCATION_LAT, LOCATION_LON, RAIN_CHECK_HOURS)
    except Exception as e:
        print(f"[ERROR] Weather check failed: {e}")
        rain_bool, rain_details = False, f"Weather check failed: {e}"

    if rain_bool:
        body = f"🌧️ Rain Alert:\n{rain_details}"
        try:
            send_sms_via_twilio(body)
            alerts_sent += 1
        except Exception as e:
            print(f"[ERROR] Failed to send rain SMS: {e}")
    else:
        print("[INFO] No rain alert. " + rain_details)

    # 2) Stock + News check
    print("[STEP] Checking stock movement & related news...")
    try:
        stock_alert, stock_payload = analyze_stock_and_get_news(STOCK_SYMBOL, COMPANY_NAME, STOCK_PERCENT_THRESHOLD)
    except Exception as e:
        print(f"[ERROR] Stock check failed: {e}")
        stock_alert, stock_payload = False, f"Stock check failed: {e}"

    if stock_alert:
        # stock_payload can be a list of messages or a single message
        if isinstance(stock_payload, list):
            for msg in stock_payload:
                try:
                    send_sms_via_twilio(msg)
                    alerts_sent += 1
                except Exception as e:
                    print(f"[ERROR] Failed to send stock SMS: {e}")
        else:
            try:
                send_sms_via_twilio(stock_payload)
                alerts_sent += 1
            except Exception as e:
                print(f"[ERROR] Failed to send stock SMS: {e}")
    else:
        print("[INFO] No stock alert. " + str(stock_payload))

    print(f"[DONE] Alerts sent: {alerts_sent}")

if __name__ == "__main__":
    main()
