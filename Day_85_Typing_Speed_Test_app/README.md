# Typing Speed Test (Desktop)

Professional typing speed test desktop app built with **Python + CustomTkinter** (dark, terminal-style UI).

## Features
- Random long paragraph from an in-code list
- Real-time character highlighting (green correct, red incorrect)
- Live WPM (5 chars/word) and Accuracy % on every keystroke
- Threaded timer (UI stays responsive)
- Personal Best (highest WPM) saved to `scores.json`
- Restart button to reset stats and load a new paragraph

## Setup

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## PyWebView + Tailwind (Pro Frontend)

This project also includes a **PyWebView** version with a web UI:
- Tailwind CSS + Lucide Icons (Carbon theme)
- Character-by-character highlighting + smooth caret
- Ghost caret at Personal Best speed
- Live WPM line graph (Chart.js) updating every second
- Scores saved via Python bridge to `scores.json`

Run it:

```bash
pip install -r requirements_webview.txt
python app_webview.py
```

Build a standalone `.exe` (PyInstaller):

```bash
python build.py
```

Important: On Windows, `pywebview` depends on `pythonnet`. If you are using a very new Python version and `pip install` fails, install **Python 3.11 or 3.12** for the PyWebView build/run.

Note: `web/index.html` currently uses Tailwind/Lucide/Chart.js via CDN. For fully offline builds, bundle those assets locally.

