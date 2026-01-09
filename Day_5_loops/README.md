## 📘 Day 5 – Sum of Even Numbers (Python Loops)

### 🧠 What I Learned
- How to use `for` loops with `range()`
- How to calculate totals using an accumulator variable
- Two different ways to find even numbers
- Using conditions (`if`) and modulus operator (`%`)
- Writing simple logic-based programs

---

## 📄 File: `Day5sumEven.py`

### 🔹 Program 1: Sum of Even Numbers (Using Step)
- Takes a target number as input
- Uses `range(0, target + 1, 2)` to loop through even numbers only
- Adds all even numbers from `0` up to the target

### 🔹 Program 2: Sum of Even Numbers (Using Condition)
- Takes a number as input
- Loops from `1` to the given number
- Uses `% 2 == 0` to check if a number is even
- Adds only even numbers to the total

---

## ▶️ How to Run
```bash
python Day5sumEven.py
python ...