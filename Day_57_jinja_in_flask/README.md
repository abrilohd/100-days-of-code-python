# Day 57 – Jinja Templating, API Integration & Blog Rendering

## 📚 What I Learned

Today I learned how to:

- Use Jinja templating with Flask
- Pass dynamic data into HTML templates
- Consume external APIs using `requests`
- Render blog posts dynamically
- Use Jinja loops and variables
- Structure multi-route Flask applications

This is a major step toward full-stack development.

---

## 📂 Project Structure

Day_57_jinja_in_flask/
│
├── main.py
├── templates/
│ ├── index.html
│ ├── guess.html
│ └── blog.html
└── static/

### 1️⃣ Dynamic Homepage

- Random number generated
- Current year displayed
- Data passed into template

---

### 2️⃣ Guess Route with API Integration
/guess/<name>

Uses:

- `genderize.io` API
- `agify.io` API

Displays:
- Predicted gender
- Estimated age

---

### 3️⃣ Blog Rendering from External API


Uses:

- `genderize.io` API
- `agify.io` API

Displays:
- Predicted gender
- Estimated age

---

### 3️⃣ Blog Rendering from External API

/blog/<num>

- Fetches blog posts from JSON API
- Renders posts dynamically using Jinja loop
- Demonstrates template-based content rendering

---

## 🛠 How to Run

```bash
pip install flask requests
python main.py

Open:

http://127.0.0.1:5000/