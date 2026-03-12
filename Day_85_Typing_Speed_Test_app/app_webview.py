import os
import random
import sqlite3
import threading
from dataclasses import dataclass
from typing import Any

import webview
import yaml


# ---------------------------------------------------------------------------
# Paths — use abspath so everything works both in dev and when compiled to .exe
# ---------------------------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(ROOT_DIR, "web")
DATA_DIR = os.path.join(ROOT_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "typing_stats.db")
CONFIG_PATH = os.path.join(ROOT_DIR, "config.yaml")


# ---------------------------------------------------------------------------
# Config — load paragraphs and window settings from config.yaml
# ---------------------------------------------------------------------------
def _load_config() -> dict[str, Any]:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


_config = _load_config()

PARAGRAPHS: list[str] = _config.get("typing", {}).get("paragraphs", [
    (
        "In the quiet hours of the morning, progress is rarely loud. It shows up as small, deliberate choices: "
        "closing an extra tab, writing a clearer function name, or taking ten minutes to understand a bug before "
        "trying to fix it. Over time, those choices compound into reliability, and reliability becomes speed."
    ),
])

_window_cfg = _config.get("app", {}).get("window", {})
WINDOW_WIDTH: int = int(_window_cfg.get("width", 1100))
WINDOW_HEIGHT: int = int(_window_cfg.get("height", 720))
WINDOW_TITLE: str = _config.get("app", {}).get("title", "Typing Speed Test — Pro")


# ---------------------------------------------------------------------------
# SQLite helpers
# ---------------------------------------------------------------------------
def _ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _init_db() -> None:
    _ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)"
    )
    conn.commit()
    conn.close()


def _get_pb() -> float:
    try:
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute(
            "SELECT value FROM settings WHERE key='personal_best_wpm'"
        ).fetchone()
        conn.close()
        return max(0.0, float(row[0])) if row else 0.0
    except Exception:
        return 0.0


def _set_pb(wpm: float) -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT OR REPLACE INTO settings (key, value) VALUES ('personal_best_wpm', ?)",
        (str(wpm),),
    )
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# App state
# ---------------------------------------------------------------------------
@dataclass
class AppState:
    personal_best_wpm: float = 0.0


# ---------------------------------------------------------------------------
# PyWebView API
# ---------------------------------------------------------------------------
class Api:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        _init_db()
        pb = _get_pb()
        self.state = AppState(personal_best_wpm=pb)

    def ping(self) -> dict[str, Any]:
        return {"ok": True}

    def get_initial_state(self) -> dict[str, Any]:
        with self._lock:
            return {"personal_best_wpm": self.state.personal_best_wpm}

    def get_paragraph(self) -> dict[str, Any]:
        text = random.choice(PARAGRAPHS)
        return {"text": text, "length": len(text)}

    def save_personal_best(self, wpm: float) -> dict[str, Any]:
        try:
            wpm_f = float(wpm)
        except Exception:
            wpm_f = 0.0
        if wpm_f < 0:
            wpm_f = 0.0

        with self._lock:
            if wpm_f > self.state.personal_best_wpm:
                self.state.personal_best_wpm = wpm_f
                _set_pb(self.state.personal_best_wpm)
            return {"personal_best_wpm": self.state.personal_best_wpm}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    api = Api()
    index = os.path.join(WEB_DIR, "index.html")
    window = webview.create_window(
        WINDOW_TITLE,
        index,
        js_api=api,
        width=WINDOW_WIDTH,
        height=WINDOW_HEIGHT,
        min_size=(900, 600),
        background_color="#323437",
    )
    webview.start(debug=False, gui=None, http_server=True)


if __name__ == "__main__":
    main()
