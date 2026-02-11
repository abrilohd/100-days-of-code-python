# Day 48 – Selenium WebDriver Automation
## 🍪 Cookie Clicker Intelligent Bot

This project is part of my 100 Days of Code journey.

Today’s focus was building a browser automation bot using Selenium WebDriver that plays the Cookie Clicker game automatically with a smart purchasing strategy.

---

## 🚀 What This Bot Does

- Continuously clicks the main cookie
- Checks available upgrades every 5 seconds
- Extracts upgrade prices dynamically from the webpage
- Calculates affordable upgrades
- Purchases the most expensive upgrade available
- Runs for 5 minutes
- Displays final Cookies Per Second (CPS)

---

## 🛠 Technologies Used

- Python 3
- Selenium WebDriver
- ChromeDriver
- Browser Automation

---

## 🧠 Key Concepts Applied

- DOM element selection
- CSS selectors and IDs
- Dynamic text parsing
- Dictionary mapping (price → item ID)
- Time-based automation loops
- Decision-based logic implementation
- Real-time webpage interaction

---

## ⚙️ Automation Logic Overview

1. Launch the Cookie Clicker webpage.
2. Click the cookie continuously.
3. Every 5 seconds:
   - Extract upgrade prices.
   - Convert text to numeric values.
   - Compare available cookies with upgrade costs.
   - Purchase the highest affordable upgrade.
4. After 5 minutes, display final CPS score.