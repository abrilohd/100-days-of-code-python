# Day 62 – Flask WTForms + CSV Data Storage

## 📌 Project Overview

This project expands Flask form handling by:

- Creating a multi-field WTForm
- Validating URLs
- Using SelectFields for ratings
- Writing submitted data to CSV
- Displaying stored data dynamically

---

## 🚀 Features

### ☕ Add Cafe Form
- Cafe name
- Location URL (validated)
- Opening & closing time
- Coffee rating (0–5)
- WiFi rating (0–5)
- Power outlet rating (0–5)
- CSRF protection

### 📁 Data Storage
- Saves entries into `cafe-data.csv`
- Appends new rows
- Displays cafes in table view

---

## 🛠 Technologies Used

- Python
- Flask
- Flask-WTF
- WTForms
- Bootstrap 5
- CSV module
- python-dotenv

---

## 🔐 Environment Setup

Create a `.env` file:

SECRET_KEY=your_random_secret_key

---

## ▶️ Installation

```bash
pip install -r requirements.txt
python main.py
Open:
http://127.0.0.1:5000/
