import json
import os
import random
import sqlite3
import threading
import time
import tkinter as tk
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import customtkinter as ctk
import yaml

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

try:
    import winsound  # Windows only
except Exception:  # pragma: no cover
    winsound = None  # type: ignore[assignment]


SCORES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.json")
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")


def clamp(n: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, n))


def _deep_get(d: dict[str, Any], path: str, default: Any) -> Any:
    cur: Any = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def load_config() -> dict[str, Any]:
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if isinstance(data, dict):
            return data
        return {}
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def resolve_path(p: str) -> str:
    if os.path.isabs(p):
        return p
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), p)


@dataclass
class LiveStats:
    elapsed_s: float = 0.0
    wpm: float = 0.0
    accuracy: float = 100.0
    burst_wpm: float = 0.0


class TypingSpeedTestApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.cfg = load_config()
        appearance = _deep_get(self.cfg, "theme.appearance_mode", "dark")
        ctk.set_appearance_mode(appearance)
        theme_json = _deep_get(self.cfg, "theme.ctk_theme_json", "dark-blue")
        try:
            ctk.set_default_color_theme(resolve_path(theme_json))
        except Exception:
            ctk.set_default_color_theme("dark-blue")

        self.title(_deep_get(self.cfg, "app.title", "Typing Speed Test"))
        w = int(_deep_get(self.cfg, "app.window.width", 980))
        h = int(_deep_get(self.cfg, "app.window.height", 640))
        self.geometry(f"{w}x{h}")
        self.minsize(860, 560)

        self._pb_wpm: float = self._load_personal_best()
        self._source_text: str = ""
        self._paragraphs: list[str] = list(_deep_get(self.cfg, "typing.paragraphs", [])) or []
        if not self._paragraphs:
            self._paragraphs = ["Config error: no paragraphs found in config.yaml"]

        self._colors = {
            "source_bg": _deep_get(self.cfg, "colors.source_bg", "#0b0f14"),
            "input_bg": _deep_get(self.cfg, "colors.input_bg", "#060a0f"),
            "border": _deep_get(self.cfg, "colors.border", "#1f2937"),
            "text_dim": _deep_get(self.cfg, "colors.text_dim", "#6b7280"),
            "text_untyped": _deep_get(self.cfg, "colors.text_untyped", "#94a3b8"),
            "text_correct": _deep_get(self.cfg, "colors.text_correct", "#22c55e"),
            "text_incorrect": _deep_get(self.cfg, "colors.text_incorrect", "#ef4444"),
            "caret_a": _deep_get(self.cfg, "colors.caret_a", "#243244"),
            "caret_b": _deep_get(self.cfg, "colors.caret_b", "#1b2533"),
            "ghost": _deep_get(self.cfg, "colors.ghost", "#38bdf8"),
        }

        self._sound_enabled = bool(_deep_get(self.cfg, "sound.enabled", False))
        self._sound_mode = str(_deep_get(self.cfg, "sound.mode", "off")).lower()
        self._beep_hz = int(_deep_get(self.cfg, "sound.beep_hz", 1200))
        self._beep_ms = int(_deep_get(self.cfg, "sound.beep_ms", 12))
        self._last_typed_len = 0
        self._sound_var = tk.BooleanVar(value=self._sound_enabled)

        self._started = False
        self._start_time: float | None = None
        self._stop_event = threading.Event()
        self._timer_thread: threading.Thread | None = None
        self._elapsed_lock = threading.Lock()
        self._elapsed_s: float = 0.0

        # Analytics state
        self._key_events: list[tuple[float, int]] = []
        self._burst_window_s = float(_deep_get(self.cfg, "analytics.burst_window_s", 5.0))
        self._burst_wpm_max: float = 0.0
        self._mistakes: dict[str, int] = {}

        self._graph_enabled = bool(_deep_get(self.cfg, "analytics.graph_enabled", True))
        self._sample_hz = float(_deep_get(self.cfg, "analytics.sample_hz", 4))
        self._sample_interval_s = 1.0 / max(1.0, self._sample_hz)
        self._last_sample_at: float = 0.0
        self._wpm_t: list[float] = []
        self._wpm_y: list[float] = []

        # Caret / ghost
        self._caret_phase = 0
        self._ghost_pos: int | None = None

        # Persistence
        self._sqlite_path = resolve_path(str(_deep_get(self.cfg, "persistence.sqlite_path", "typing_sessions.db")))
        self._db = self._init_db(self._sqlite_path)

        self._build_ui()
        self.restart()

        self.after(100, self._ui_tick)
        self.after(160, self._caret_pulse_tick)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self, corner_radius=12)
        header.grid(row=0, column=0, padx=16, pady=(16, 10), sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        title = ctk.CTkLabel(
            header,
            text="Typing Speed Test",
            font=ctk.CTkFont(family="Consolas", size=26, weight="bold"),
        )
        title.grid(row=0, column=0, padx=14, pady=12, sticky="w")

        self.restart_btn = ctk.CTkButton(
            header,
            text="Restart",
            command=self.restart,
            width=120,
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
        )
        self.restart_btn.grid(row=0, column=1, padx=14, pady=12, sticky="e")

        self.sound_switch = ctk.CTkSwitch(
            header,
            text="Sound",
            variable=self._sound_var,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
        )
        self.sound_switch.grid(row=0, column=2, padx=(0, 14), pady=12, sticky="e")

        stats = ctk.CTkFrame(self, corner_radius=12)
        stats.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="ew")
        for i in range(6):
            stats.grid_columnconfigure(i, weight=1)

        self.time_lbl = self._stat_cell(stats, 0, "Time", "0.0s")
        self.wpm_lbl = self._stat_cell(stats, 1, "WPM", "0.0")
        self.acc_lbl = self._stat_cell(stats, 2, "Accuracy", "100.0%")
        self.pb_lbl = self._stat_cell(stats, 3, "Personal Best", f"{self._pb_wpm:.1f}")
        self.progress_lbl = self._stat_cell(stats, 4, "Progress", "0 / 0")
        self.burst_lbl = self._stat_cell(stats, 5, "Burst (5s)", "0.0")

        body = ctk.CTkFrame(self, corner_radius=12)
        body.grid(row=2, column=0, padx=16, pady=(0, 16), sticky="nsew")
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(1, weight=1)
        body.grid_rowconfigure(3, weight=1)

        src_label = ctk.CTkLabel(
            body,
            text="Source text",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            anchor="w",
        )
        src_label.grid(row=0, column=0, padx=14, pady=(14, 6), sticky="ew")

        self.source_box = ctk.CTkTextbox(
            body,
            height=160,
            wrap="word",
            font=ctk.CTkFont(family="Consolas", size=14),
            fg_color=self._colors["source_bg"],
            text_color=self._colors["text_untyped"],
            corner_radius=10,
            border_width=1,
            border_color=self._colors["border"],
        )
        self.source_box.grid(row=1, column=0, padx=14, pady=(0, 12), sticky="nsew")
        self._init_source_tags()

        input_label = ctk.CTkLabel(
            body,
            text="Type here",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            anchor="w",
        )
        input_label.grid(row=2, column=0, padx=14, pady=(0, 6), sticky="ew")

        self.input_box = ctk.CTkTextbox(
            body,
            wrap="word",
            font=ctk.CTkFont(family="Consolas", size=14),
            fg_color=self._colors["input_bg"],
            text_color="#e5e7eb",
            corner_radius=10,
            border_width=1,
            border_color=self._colors["border"],
        )
        self.input_box.grid(row=3, column=0, padx=14, pady=(0, 14), sticky="nsew")
        try:
            input_tb: tk.Text = self.input_box._textbox  # type: ignore[attr-defined]
            input_tb.configure(insertbackground="#e5e7eb")
        except Exception:
            pass
        self.input_box.bind("<KeyRelease>", self._on_input_changed)
        self.input_box.bind("<Control-a>", self._select_all)
        self.input_box.bind("<Control-A>", self._select_all)

        # Analytics panel (right column)
        panel = ctk.CTkFrame(body, corner_radius=12, fg_color=self._colors["source_bg"])
        panel.grid(row=0, column=1, rowspan=4, padx=(0, 14), pady=14, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)

        panel_title = ctk.CTkLabel(
            panel,
            text="Analytics",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            anchor="w",
        )
        panel_title.grid(row=0, column=0, padx=12, pady=(12, 6), sticky="ew")

        self._build_graph(panel)

        self.weaks_label = ctk.CTkLabel(
            panel,
            text="Weaknesses will appear after a run.",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#9aa4b2",
            justify="left",
            anchor="nw",
        )
        self.weaks_label.grid(row=2, column=0, padx=12, pady=(8, 12), sticky="ew")

    def _stat_cell(self, parent: ctk.CTkFrame, col: int, label: str, value: str) -> ctk.CTkLabel:
        cell = ctk.CTkFrame(parent, corner_radius=10, fg_color="#0b0f14")
        cell.grid(row=0, column=col, padx=(12 if col == 0 else 6, 6), pady=12, sticky="ew")
        cell.grid_columnconfigure(0, weight=1)

        lbl = ctk.CTkLabel(
            cell,
            text=label,
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color="#9aa4b2",
            anchor="w",
        )
        lbl.grid(row=0, column=0, padx=10, pady=(8, 2), sticky="ew")

        val = ctk.CTkLabel(
            cell,
            text=value,
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color="#e5e7eb",
            anchor="w",
        )
        val.grid(row=1, column=0, padx=10, pady=(0, 8), sticky="ew")
        return val

    def _init_source_tags(self) -> None:
        tb: tk.Text = self.source_box._textbox  # type: ignore[attr-defined]
        tb.configure(state="normal")
        tb.tag_configure("dim", foreground=self._colors["text_dim"])
        tb.tag_configure("untyped", foreground=self._colors["text_untyped"])
        tb.tag_configure("correct", foreground=self._colors["text_correct"])
        tb.tag_configure("incorrect", foreground=self._colors["text_incorrect"])
        tb.tag_configure("caret", background=self._colors["caret_a"])
        tb.tag_configure("ghost", background="", underline=True, foreground=self._colors["ghost"])
        tb.configure(state="disabled")

    def _set_source_text(self, text: str) -> None:
        self._source_text = text
        tb: tk.Text = self.source_box._textbox  # type: ignore[attr-defined]
        tb.configure(state="normal")
        tb.delete("1.0", "end")
        tb.insert("1.0", text)
        tb.tag_add("dim", "1.0", "end")
        tb.tag_add("untyped", "1.0", "end")
        tb.configure(state="disabled")
        self._apply_highlighting("")

    def _get_input(self) -> str:
        return self.input_box.get("1.0", "end-1c")

    def _clear_input(self) -> None:
        self.input_box.delete("1.0", "end")

    def _select_all(self, event: tk.Event) -> str:
        self.input_box.tag_add("sel", "1.0", "end-1c")
        return "break"

    def _on_input_changed(self, _event: tk.Event) -> None:
        typed = self._get_input()

        if len(typed) > len(self._source_text):
            typed = typed[: len(self._source_text)]
            self.input_box.delete("1.0", "end")
            self.input_box.insert("1.0", typed)
            self.input_box._textbox.mark_set("insert", "end-1c")  # type: ignore[attr-defined]

        if bool(self._sound_var.get()) and self._sound_mode != "off":
            if len(typed) > self._last_typed_len:
                self._play_click()
        self._last_typed_len = len(typed)

        if not self._started and typed:
            self._start()

        self._record_event(typed)
        self._apply_highlighting(typed)
        stats = self._compute_stats(typed)
        self._render_stats(typed, stats)

        if typed == self._source_text and self._started:
            self._finish(stats)

    def _compute_stats(self, typed: str) -> LiveStats:
        with self._elapsed_lock:
            elapsed_s = self._elapsed_s

        if elapsed_s <= 0:
            elapsed_s = 0.0

        total_typed = len(typed)
        correct = 0
        limit = min(total_typed, len(self._source_text))
        src = self._source_text
        for i in range(limit):
            if typed[i] == src[i]:
                correct += 1

        # WPM standardized: 5 chars = 1 word; use all typed chars (including incorrect)
        minutes = elapsed_s / 60.0 if elapsed_s > 0 else 0.0
        wpm = (total_typed / 5.0) / minutes if minutes > 0 else 0.0

        accuracy = (correct / total_typed) * 100.0 if total_typed > 0 else 100.0
        accuracy = clamp(accuracy, 0.0, 100.0)

        burst = self._burst_wpm_max if self._started else 0.0
        return LiveStats(elapsed_s=elapsed_s, wpm=wpm, accuracy=accuracy, burst_wpm=burst)

    def _render_stats(self, typed: str, stats: LiveStats) -> None:
        self.time_lbl.configure(text=f"{stats.elapsed_s:.1f}s")
        self.wpm_lbl.configure(text=f"{stats.wpm:.1f}")
        self.acc_lbl.configure(text=f"{stats.accuracy:.1f}%")
        self.pb_lbl.configure(text=f"{self._pb_wpm:.1f}")
        self.progress_lbl.configure(text=f"{len(typed)} / {len(self._source_text)}")
        self.burst_lbl.configure(text=f"{stats.burst_wpm:.1f}")

    def _apply_highlighting(self, typed: str) -> None:
        tb: tk.Text = self.source_box._textbox  # type: ignore[attr-defined]
        tb.configure(state="normal")

        tb.tag_remove("correct", "1.0", "end")
        tb.tag_remove("incorrect", "1.0", "end")
        tb.tag_remove("caret", "1.0", "end")
        tb.tag_remove("ghost", "1.0", "end")

        n = len(typed)
        src_len = len(self._source_text)
        limit = min(n, src_len)

        for i in range(limit):
            tag = "correct" if typed[i] == self._source_text[i] else "incorrect"
            start = f"1.0+{i}c"
            end = f"1.0+{i+1}c"
            tb.tag_add(tag, start, end)

        if n < src_len:
            caret_start = f"1.0+{n}c"
            caret_end = f"1.0+{n+1}c"
            tb.tag_add("caret", caret_start, caret_end)

        ghost_pos = self._ghost_position()
        if ghost_pos is not None and 0 <= ghost_pos < src_len and ghost_pos != n:
            tb.tag_add("ghost", f"1.0+{ghost_pos}c", f"1.0+{ghost_pos+1}c")

        tb.configure(state="disabled")

        if n > 0:
            try:
                tb.see(f"1.0+{max(0, n-20)}c")
            except tk.TclError:
                pass

    def _start(self) -> None:
        self._started = True
        self._start_time = time.perf_counter()
        self._stop_event.clear()
        self._key_events = [(0.0, 0)]
        self._burst_wpm_max = 0.0
        self._mistakes = {}
        self._wpm_t = []
        self._wpm_y = []
        self._last_sample_at = 0.0

        if self._timer_thread and self._timer_thread.is_alive():
            return

        self._timer_thread = threading.Thread(target=self._timer_worker, daemon=True)
        self._timer_thread.start()

    def _finish(self, stats: LiveStats) -> None:
        self._stop_event.set()

        final_wpm = stats.wpm
        if final_wpm > self._pb_wpm:
            self._pb_wpm = final_wpm
            self._save_personal_best(self._pb_wpm)
            self.pb_lbl.configure(text=f"{self._pb_wpm:.1f}")

        self._persist_session(stats)
        self._render_weaknesses()
        self._show_summary(stats)

    def _timer_worker(self) -> None:
        while not self._stop_event.is_set():
            if self._start_time is None:
                time.sleep(0.05)
                continue

            now = time.perf_counter()
            with self._elapsed_lock:
                self._elapsed_s = now - self._start_time
            time.sleep(0.05)

    def _ui_tick(self) -> None:
        typed = self._get_input()
        if self._started and not self._stop_event.is_set():
            stats = self._compute_stats(typed)
            self._render_stats(typed, stats)
            self._maybe_sample_wpm(stats)
            self._update_graph()
        self.after(100, self._ui_tick)

    def restart(self) -> None:
        self._stop_event.set()
        self._started = False
        self._start_time = None

        with self._elapsed_lock:
            self._elapsed_s = 0.0

        paragraph = random.choice(self._paragraphs)
        self._set_source_text(paragraph)

        self._clear_input()
        self._render_stats("", LiveStats(elapsed_s=0.0, wpm=0.0, accuracy=100.0))
        self._last_typed_len = 0
        self._key_events = [(0.0, 0)]
        self._burst_wpm_max = 0.0
        self._mistakes = {}
        self._wpm_t = []
        self._wpm_y = []
        self._last_sample_at = 0.0
        self._clear_graph()
        self.weaks_label.configure(text="Weaknesses will appear after a run.")
        self.input_box.focus_set()

    def _play_click(self) -> None:
        if self._sound_mode == "beep" and winsound is not None:
            try:
                winsound.Beep(self._beep_hz, self._beep_ms)
            except Exception:
                pass

    def _caret_pulse_tick(self) -> None:
        self._caret_phase = 1 - self._caret_phase
        tb: tk.Text = self.source_box._textbox  # type: ignore[attr-defined]
        try:
            tb.tag_configure("caret", background=self._colors["caret_b" if self._caret_phase else "caret_a"])
        except Exception:
            pass
        self.after(160, self._caret_pulse_tick)

    def _ghost_position(self) -> int | None:
        with self._elapsed_lock:
            elapsed_s = self._elapsed_s
        if elapsed_s <= 0 or self._pb_wpm <= 0 or not self._started:
            return None
        chars_per_min = self._pb_wpm * 5.0
        ghost_chars = int((chars_per_min / 60.0) * elapsed_s)
        ghost_chars = min(max(0, ghost_chars), len(self._source_text))
        return ghost_chars

    def _record_event(self, typed: str) -> None:
        if not self._started or self._start_time is None:
            return
        t = time.perf_counter() - self._start_time
        n = len(typed)

        # Only count a mistake when user *adds* a character at a new position.
        prev_n = self._key_events[-1][1] if self._key_events else 0
        if n > prev_n:
            i = n - 1
            if 0 <= i < len(self._source_text):
                expected = self._source_text[i]
                got = typed[i]
                if expected != got:
                    self._mistakes[expected] = self._mistakes.get(expected, 0) + 1

        self._key_events.append((t, n))
        self._update_burst_from_events()

    def _update_burst_from_events(self) -> None:
        if len(self._key_events) < 2:
            return
        t_now, n_now = self._key_events[-1]
        window = self._burst_window_s

        # Find earliest event still in window
        j = len(self._key_events) - 1
        while j > 0 and (t_now - self._key_events[j - 1][0]) <= window:
            j -= 1
        t_old, n_old = self._key_events[j]
        dt = max(0.001, t_now - t_old)
        dn = max(0, n_now - n_old)
        wpm_window = (dn / 5.0) / (dt / 60.0)
        if wpm_window > self._burst_wpm_max:
            self._burst_wpm_max = wpm_window

    def _build_graph(self, parent: ctk.CTkFrame) -> None:
        self._fig = Figure(figsize=(4.2, 2.5), dpi=100)
        self._fig.patch.set_facecolor(self._colors["source_bg"])
        self._ax = self._fig.add_subplot(111)
        self._ax.set_facecolor(self._colors["source_bg"])
        self._ax.tick_params(colors="#9aa4b2", labelsize=8)
        for spine in self._ax.spines.values():
            spine.set_color(self._colors["border"])
        self._ax.grid(True, color="#111827", linewidth=0.8, alpha=0.8)
        self._ax.set_title("WPM volatility", color="#cbd5e1", fontsize=10, pad=8)
        self._ax.set_xlabel("t (s)", color="#9aa4b2", fontsize=8)
        self._ax.set_ylabel("WPM", color="#9aa4b2", fontsize=8)
        (self._line,) = self._ax.plot([], [], color="#38bdf8", linewidth=2)
        self._ax.set_xlim(0, 30)
        self._ax.set_ylim(0, 120)

        self._canvas = FigureCanvasTkAgg(self._fig, master=parent)
        self._canvas_widget = self._canvas.get_tk_widget()
        self._canvas_widget.configure(background=self._colors["source_bg"], highlightthickness=0)
        self._canvas_widget.grid(row=1, column=0, padx=12, pady=(0, 8), sticky="nsew")

    def _clear_graph(self) -> None:
        if hasattr(self, "_line"):
            self._line.set_data([], [])
        if hasattr(self, "_canvas"):
            try:
                self._canvas.draw_idle()
            except Exception:
                pass

    def _maybe_sample_wpm(self, stats: LiveStats) -> None:
        if not self._graph_enabled or self._start_time is None:
            return
        now = time.perf_counter() - self._start_time
        if (now - self._last_sample_at) < self._sample_interval_s:
            return
        self._last_sample_at = now
        self._wpm_t.append(now)
        self._wpm_y.append(stats.wpm)

    def _update_graph(self) -> None:
        if not self._graph_enabled or not hasattr(self, "_line"):
            return
        if not self._wpm_t:
            return
        self._line.set_data(self._wpm_t, self._wpm_y)
        tmax = max(10.0, self._wpm_t[-1])
        self._ax.set_xlim(max(0.0, tmax - 30.0), tmax + 1.0)
        ymax = max(60.0, max(self._wpm_y) * 1.15)
        self._ax.set_ylim(0.0, min(240.0, ymax))
        try:
            self._canvas.draw_idle()
        except Exception:
            pass

    def _render_weaknesses(self) -> None:
        if not self._mistakes:
            self.weaks_label.configure(text="No mistakes recorded. Clean run.")
            return
        top = sorted(self._mistakes.items(), key=lambda kv: kv[1], reverse=True)[:8]
        lines = ["Top weaknesses (most missed expected chars):"]
        for ch, cnt in top:
            shown = ch
            if shown == " ":
                shown = "<space>"
            elif shown == "\n":
                shown = "<newline>"
            lines.append(f"- {shown!s}: {cnt}")
        self.weaks_label.configure(text="\n".join(lines))

    def _init_db(self, path: str) -> sqlite3.Connection:
        conn = sqlite3.connect(path, check_same_thread=False)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              started_at_utc TEXT NOT NULL,
              source_len INTEGER NOT NULL,
              elapsed_s REAL NOT NULL,
              wpm REAL NOT NULL,
              accuracy REAL NOT NULL,
              burst_wpm REAL NOT NULL,
              personal_best_wpm REAL NOT NULL,
              mistakes_json TEXT NOT NULL
            )
            """
        )
        conn.commit()
        return conn

    def _persist_session(self, stats: LiveStats) -> None:
        started = datetime.now(timezone.utc).isoformat()
        mistakes_json = json.dumps(self._mistakes, ensure_ascii=False)
        try:
            self._db.execute(
                """
                INSERT INTO sessions (
                  started_at_utc, source_len, elapsed_s, wpm, accuracy, burst_wpm, personal_best_wpm, mistakes_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    started,
                    len(self._source_text),
                    float(stats.elapsed_s),
                    float(stats.wpm),
                    float(stats.accuracy),
                    float(stats.burst_wpm),
                    float(self._pb_wpm),
                    mistakes_json,
                ),
            )
            self._db.commit()
        except Exception:
            pass

    def _show_summary(self, stats: LiveStats) -> None:
        top = ctk.CTkToplevel(self)
        top.title("Summary")
        top.geometry("520x420")
        top.resizable(False, False)
        top.transient(self)
        top.grab_set()
        top.attributes("-alpha", 0.0)

        frame = ctk.CTkFrame(top, corner_radius=14)
        frame.pack(fill="both", expand=True, padx=16, pady=16)

        title = ctk.CTkLabel(
            frame,
            text="Summary Dashboard",
            font=ctk.CTkFont(family="Consolas", size=20, weight="bold"),
        )
        title.pack(pady=(18, 10))

        metrics = [
            ("Sustained WPM", f"{stats.wpm:.1f}"),
            ("Burst WPM (5s)", f"{stats.burst_wpm:.1f}"),
            ("Accuracy", f"{stats.accuracy:.1f}%"),
            ("Time", f"{stats.elapsed_s:.1f}s"),
            ("Personal Best", f"{self._pb_wpm:.1f}"),
        ]
        for k, v in metrics:
            row = ctk.CTkFrame(frame, corner_radius=10, fg_color=self._colors["source_bg"])
            row.pack(fill="x", padx=18, pady=6)
            ctk.CTkLabel(row, text=k, font=ctk.CTkFont(family="Consolas", size=12, weight="bold"), text_color="#9aa4b2").pack(
                side="left", padx=12, pady=10
            )
            ctk.CTkLabel(row, text=v, font=ctk.CTkFont(family="Consolas", size=14, weight="bold")).pack(
                side="right", padx=12, pady=10
            )

        weak_text = self.weaks_label.cget("text")
        weak_box = ctk.CTkTextbox(
            frame,
            height=110,
            wrap="word",
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=self._colors["input_bg"],
            text_color="#cbd5e1",
            border_width=1,
            border_color=self._colors["border"],
        )
        weak_box.pack(fill="x", padx=18, pady=(10, 10))
        weak_box.insert("1.0", weak_text)
        weak_box.configure(state="disabled")

        btns = ctk.CTkFrame(frame, fg_color="transparent")
        btns.pack(fill="x", padx=18, pady=(0, 18))
        ctk.CTkButton(btns, text="Restart", command=lambda: (top.destroy(), self.restart())).pack(side="right")
        ctk.CTkButton(btns, text="Close", fg_color="#0b0f14", hover_color="#111827", command=top.destroy).pack(
            side="right", padx=(0, 8)
        )

        def fade(alpha: float) -> None:
            alpha = clamp(alpha, 0.0, 0.96)
            try:
                top.attributes("-alpha", alpha)
            except Exception:
                return
            if alpha < 0.96:
                top.after(16, lambda: fade(alpha + 0.06))

        fade(0.0)

    def _load_personal_best(self) -> float:
        try:
            with open(SCORES_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            pb = float(data.get("personal_best_wpm", 0.0))
            return max(0.0, pb)
        except FileNotFoundError:
            return 0.0
        except (json.JSONDecodeError, ValueError, TypeError):
            return 0.0

    def _save_personal_best(self, pb_wpm: float) -> None:
        tmp_path = SCORES_PATH + ".tmp"
        data = {"personal_best_wpm": float(pb_wpm)}
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_path, SCORES_PATH)

    def _on_close(self) -> None:
        self._stop_event.set()
        try:
            self._db.close()
        except Exception:
            pass
        self.destroy()


def main() -> None:
    app = TypingSpeedTestApp()
    app.mainloop()


if __name__ == "__main__":
    main()

