# Day 53 – Real Estate Data Collector Bot

## 🚀 Overview

This project scrapes property listings from a Zillow clone website and automatically submits the data into a Google Form.

The bot:
- Scrapes price, address, and listing links
- Extracts structured data using BeautifulSoup
- Automates Google Form submission using Selenium
- Creates a structured data collection pipeline

## 🛠 Tech Stack

- Python
- Requests
- BeautifulSoup
- Selenium WebDriver

## ⚙ How It Works

1. Send HTTP request to property listing page
2. Parse HTML content
3. Extract:
   - Price
   - Address
   - Property Link
4. Open Google Form
5. Submit each listing automatically

## ▶️ Run

pip install -r requirements.txt  
python main.py

## 🧠 Concepts Practiced

- Web scraping
- HTML parsing
- CSS selectors
- Data extraction pipelines
- Browser automation
- Form automation

## 📈 Improvements

- Add exception handling
- Convert to CSV storage
- Add headless mode
- Add retry mechanism
- Implement logging system
- Use environment variables instead of hardcoded URLs
