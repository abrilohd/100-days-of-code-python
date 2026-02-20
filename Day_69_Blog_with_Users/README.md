# 📝 Day 69 – Blog with Users & Comments

A full-stack Flask blog application with:

- User registration & login
- Password hashing
- Blog post creation
- Comment system
- Relational database (User ↔ Posts ↔ Comments)
- Admin-restricted post management

---

## 🚀 Features

### 🔐 Authentication
- Secure user registration
- Login/logout system
- Password hashing using Werkzeug

### 📰 Blog System
- Create posts (Admin only)
- Edit posts
- Delete posts
- View individual posts

### 💬 Comment System
- Logged-in users can comment
- Comments linked to users and posts
- Relationship-based database design

---

## 🛠 Tech Stack

- Python
- Flask
- Flask-WTF
- Flask-Login
- Flask-SQLAlchemy
- Flask-CKEditor
- Bootstrap

---

## 📂 Database Structure

### User
- id
- email
- password
- name
- relationship → posts
- relationship → comments

### BlogPost
- id
- title
- subtitle
- img_url
- body
- author_id
- relationship → comments

### Comment
- id
- text
- author_id
- post_id

---

## ▶ Installation

```bash
pip install -r requirements.txt
▶ Run Application
python main.py
Open:
http://localhost:5001