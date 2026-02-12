# Day 50 – Tinder Automation Bot

### 📌 Overview
This project automates interactions on Tinder using [Selenium WebDriver](https://www.selenium.dev). It handles login via Facebook, manages browser window switching, and performs automated liking actions.

> [!WARNING]  
> Built for educational automation purposes only. Please review [Tinder's Terms of Service](https://policies.tinder.com) before use.

### 🛠 Technologies Used
Python
[Selenium WebDriver](https://pypi.org) – Browser automation
ChromeDriver – Interface for Chrome browser control
[python-dotenv](https://github.com) – Environment variable management for credential security

### ⚙️ Features
Automated Login: Signs in via Facebook integration
Multi-window Handling: Switches between the main app and login popups
CAPTCHA Wait Handling: Pauses for manual verification when triggered
Automated Like Actions: Systematic swiping functionality
Exception Handling: Manages unexpected popups (e.g., Add to Home Screen)
Rate Limiting Awareness: Built to respect daily swiping thresholds
