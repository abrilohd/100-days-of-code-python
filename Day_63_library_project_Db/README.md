# Day 63 – Flask Library Database (SQLAlchemy)

## 📌 Project Overview

This project upgrades previous CSV storage to a real database using SQLAlchemy.

It implements:

- SQLite database integration
- ORM model creation
- CRUD operations
- WTForms validation
- Book rating system

---

## 🚀 Features

### 📚 Book Management
- Add books
- Edit rating
- Delete books
- View all books
- Sorted by rating (highest first)

### 🛡 Validation
- Required fields
- Rating range validation (0–10)
- CSRF protection

### 🗄 Database
- SQLite database (`books.db`)
- SQLAlchemy ORM
- Automatic table creation

---

## 🛠 Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- WTForms
- Bootstrap 5
- SQLite

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
