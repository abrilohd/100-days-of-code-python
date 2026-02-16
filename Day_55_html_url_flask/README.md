# Day 55 – HTML, Dynamic URLs & Advanced Decorators (Flask)

## 📚 What I Learned

Today I learned:

- How to build a simple Flask web app
- How to use dynamic URL routes (`/<int:guess>`)
- How to return HTML directly from routes
- How to apply custom decorators to Flask routes
- How decorator order affects output
- How to create authentication-like decorators using `*args, **kwargs`

---

## 🚀 Project 1 – Guess The Number (Flask Web App)

### Description

A simple browser-based guessing game:
- The server generates a random number between 0–9
- The user guesses via URL
- The page responds with:
  - Too high
  - Too low
  - Correct

### Example

http://127.0.0.1:5000/5


### Concepts Practiced

- `@app.route`
- Dynamic URL parameters
- Conditional rendering
- Inline HTML styling

---

## 🚀 Project 2 – HTML Decorator Styling

Created custom decorators:

- `@bold`
- `@under_line`
- `@make_enphasis`

Stacked them on a Flask route:

```python
@app.route("/bye")
@bold
@under_line
@make_enphasis
def bye():
    return "Bye see you"
