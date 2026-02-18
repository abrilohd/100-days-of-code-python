# Day 64 – Movie Ranking Website (TMDB API + Database)

## 📌 Project Overview

This project integrates:

- External Movie API (TMDB)
- SQLite database with SQLAlchemy
- Movie search & selection
- Rating & review system
- Dynamic ranking system

---

## 🚀 Features

### 🎬 Movie Search
- Search movie via TMDB API
- Select from results
- Auto-import movie details

### 🗄 Database
- SQLite storage
- SQLAlchemy ORM
- Auto ranking system
- Duplicate prevention

### ⭐ Rating System
- Rate movies (0–10)
- Add personal reviews
- Ranking updates automatically

---

## 🛠 Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-WTF
- Requests
- Bootstrap 5
- TMDB API

---

## 🔐 Environment Variables (.env)

SECRET_KEY=your_secret_key
TMDB_API_KEY=your_tmdb_key
TMDB_SEARCH_URL=https://api.themoviedb.org/3/search/movie

TMDB_INFO_URL=https://api.themoviedb.org/3/movie/

TMDB_IMAGE_URL=https://image.tmdb.org/t/p/w500

---

## ▶️ Installation

```bash
pip install -r requirements.txt
python main.py
Visit:

http://127.0.0.1:5000/