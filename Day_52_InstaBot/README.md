# 📄 README.md

*(Production-Ready | Portfolio-Safe | Future-Proof)*

## 🚀 Project Summary

This project automates follower interaction on Instagram using Selenium WebDriver.

The bot:
- Logs into Instagram securely
- Navigates to a target profile
- Opens the followers modal
- Scrolls dynamically to load accounts
- Automatically follows visible users
- Handles modal interruptions safely

## 🎯 Learning Objectives

- Advanced DOM interaction
- Infinite scroll automation
- Modal window handling
- Exception management
- Credential security using `.env`
- Class-based automation structure

## 🏗 Project Structure
Day_52_InstaBot/
│
├── main.py
├── README.md
├── IDEAS.md
└── .env (excluded from Git)


## 🔐 Environment Setup

Create a `.env` file:
INSTA_USERNAME=your_username
INSTA_PASSWORD=your_password


Add `.env` to `.gitignore`.

### Install dependencies:

```bash
pip install selenium python-dotenv webdriver-manager