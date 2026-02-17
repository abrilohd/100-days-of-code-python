# Day 61 – Flask WTForms & Form Validation

## 📌 Project Overview

This project introduces:

- Flask-WTF form handling
- CSRF protection
- WTForms validation
- Bootstrap form styling
- Secure login validation flow

---

## 🚀 Features

### 🔐 Login System
- Email validation
- Password length validation
- CSRF protection
- Styled with Bootstrap 5
- Success & denied pages

### 🛡 Security Improvements
- Secret key via environment variable
- Form validation before processing
- Protection against empty input
- Clean route structure

---

## 🛠 Technologies Used

- Python
- Flask
- Flask-WTF
- WTForms
- Bootstrap 5
- python-dotenv

---

## 🔐 Environment Setup

Create a `.env` file:
SECRET_KEY=your_random_secret_key_here


---

## ▶️ Installation

```bash
pip install -r requirements.txt
python main.py

visit:
http://127.0.0.1:5000/login
