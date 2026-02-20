# Day 66 – Building a REST API with Flask

## 📌 Overview

This project builds a fully functional RESTful API using Flask and SQLAlchemy.

The API allows users to:

- Retrieve cafe data
- Search by location
- Add new cafes
- Update prices
- Delete records (protected by API key)

---

## 🚀 API Endpoints

### GET
- `/random` → Get a random cafe
- `/all` → Get all cafes
- `/search?loc=City` → Search by location

### POST
- `/add` → Add new cafe

### PATCH
- `/update-price/<id>?new_price=£3.50`

### DELETE
- `/report-closed/<id>?api-key=YOUR_KEY`

---

## 🗄 Database

- SQLite (`cafes.db`)
- SQLAlchemy ORM
- Auto table creation

---

## 🔐 Environment Variables (.env)
API_KEY=YourSecretAPIKey


---

## ▶️ Installation

```bash
pip install -r requirements.txt
python main.py