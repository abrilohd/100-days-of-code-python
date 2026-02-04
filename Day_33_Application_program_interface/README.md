# Day 33 – Working with APIs 🌐

## What I Built
Two Python projects that consume public APIs to build real-world applications:
1. ISS Overhead Notifier (Automation + Email)
2. Kanye Quotes App (API + GUI)

## Projects Included

### 1️⃣ ISS Overhead Notifier
A background script that checks:
- The real-time location of the ISS
- Whether it is currently night at my location  
If both conditions are true, it sends an email alert to look up at the sky.

**Concepts used:**
- REST APIs (`requests`)
- JSON data handling
- Datetime and time-based automation
- SMTP email sending

### 2️⃣ Kanye Quotes GUI
A simple Tkinter application that fetches and displays random Kanye West quotes from a public API every time the button is clicked.

**Concepts used:**
- API requests
- Tkinter GUI
- Event-driven programming
- Error handling with `raise_for_status()`

## Why This Matters
These projects demonstrate how APIs power real applications such as notifications, dashboards, and interactive user interfaces.
