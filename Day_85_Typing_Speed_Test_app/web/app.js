/* global Chart */

const $ = (id) => document.getElementById(id);

const state = {
  source: "",
  spans: [],
  started: false,
  finished: false,
  startTs: 0,
  elapsedS: 0,
  pbWpm: 0,
  typed: "",
  correct: 0,
  mistakes: new Map(), // expected char -> count
  events: [{ t: 0, n: 0 }], // for burst window
  burstMax: 0,
  ghostEnabled: true,
  graph: {
    labels: [],
    data: [],
    timer: null,
  },
  tickTimer: null,
  lastStats: { wpm: null, acc: null },
};

function clamp(n, lo, hi) {
  return Math.max(lo, Math.min(hi, n));
}

function nowMs() {
  return performance.now();
}

function fmtChar(ch) {
  if (ch === " ") return "<space>";
  if (ch === "\n") return "<newline>";
  if (ch === "\t") return "<tab>";
  return ch;
}

async function apiCall(method, ...args) {
  if (!window.pywebview || !window.pywebview.api || !window.pywebview.api[method]) {
    throw new Error("PyWebView bridge not available");
  }
  return await window.pywebview.api[method](...args);
}

function buildSourceSpans(text) {
  const container = $("sourceText");
  container.textContent = "";
  const frag = document.createDocumentFragment();

  const spans = [];
  for (let i = 0; i < text.length; i++) {
    const s = document.createElement("span");
    s.textContent = text[i];
    s.className = "char-untyped";
    s.dataset.idx = String(i);
    spans.push(s);
    frag.appendChild(s);
  }

  container.appendChild(frag);
  return spans;
}

function computeStats() {
  const n = state.typed.length;
  const correct = state.correct;

  const minutes = state.elapsedS > 0 ? state.elapsedS / 60 : 0;
  const wpm = minutes > 0 ? (n / 5) / minutes : 0;
  const acc = n > 0 ? (correct / n) * 100 : 100;

  return { wpm, acc: clamp(acc, 0, 100), n };
}

function updateStatsUI() {
  const { wpm, acc, n } = computeStats();
  $("statTime").textContent = `${state.elapsedS.toFixed(1)}s`;
  $("statWpm").textContent = wpm.toFixed(1);
  $("statAcc").textContent = `${acc.toFixed(1)}%`;
  $("statPb").textContent = state.pbWpm.toFixed(1);
  $("progress").textContent = `${n} / ${state.source.length}`;

  // pulse when changed
  const wpmEl = $("statWpm");
  const accEl = $("statAcc");
  if (state.lastStats.wpm !== null && Math.abs(state.lastStats.wpm - wpm) >= 0.1) {
    wpmEl.classList.remove("pulse");
    void wpmEl.offsetWidth;
    wpmEl.classList.add("pulse");
  }
  if (state.lastStats.acc !== null && Math.abs(state.lastStats.acc - acc) >= 0.1) {
    accEl.classList.remove("pulse");
    void accEl.offsetWidth;
    accEl.classList.add("pulse");
  }
  state.lastStats.wpm = wpm;
  state.lastStats.acc = acc;
}

function updateBurst() {
  const windowS = 5.0;
  const events = state.events;
  if (events.length < 2) return;

  const last = events[events.length - 1];
  const tNow = last.t;
  const nNow = last.n;

  let j = events.length - 1;
  while (j > 0 && (tNow - events[j - 1].t) <= windowS) {
    j--;
  }
  const old = events[j];
  const dt = Math.max(0.001, tNow - old.t);
  const dn = Math.max(0, nNow - old.n);
  const wpm = (dn / 5) / (dt / 60);
  if (wpm > state.burstMax) state.burstMax = wpm;
}

function applyHighlighting() {
  const spans = state.spans;
  const src = state.source;
  const typed = state.typed;
  const limit = Math.min(typed.length, src.length);

  for (let i = 0; i < spans.length; i++) {
    const s = spans[i];
    if (i < limit) {
      const ok = typed[i] === src[i];
      s.className = ok ? "char-correct" : "char-wrong";
    } else {
      s.className = "char-untyped";
    }
  }
}

function getCaretTargetRect(idx) {
  // idx is the insertion position (0..len)
  const wrap = $("sourceWrap");
  const container = $("sourceText");

  if (state.spans.length === 0) return null;
  if (idx >= state.spans.length) {
    const last = state.spans[state.spans.length - 1];
    const r = last.getBoundingClientRect();
    return { left: r.right, top: r.top, wrap, container };
  }

  const span = state.spans[idx];
  const r = span.getBoundingClientRect();
  return { left: r.left, top: r.top, wrap, container };
}

function moveCaret() {
  const caret = $("caret");
  const idx = state.typed.length;
  const info = getCaretTargetRect(idx);
  if (!info) return;

  const wrapRect = info.wrap.getBoundingClientRect();
  const x = info.left - wrapRect.left + info.wrap.scrollLeft;
  const y = info.top - wrapRect.top + info.wrap.scrollTop;

  caret.style.left = `${Math.round(x)}px`;
  caret.style.top = `${Math.round(y)}px`;

  // keep caret in view
  const pad = 28;
  const targetY = y;
  if (targetY < info.wrap.scrollTop + pad) info.wrap.scrollTop = Math.max(0, targetY - pad);
  const maxY = info.wrap.scrollTop + info.wrap.clientHeight - pad;
  if (targetY > maxY) info.wrap.scrollTop = targetY - info.wrap.clientHeight + pad;
}

function moveGhostCaret() {
  const ghost = $("ghostCaret");
  if (!state.ghostEnabled || !state.started || state.pbWpm <= 0) {
    ghost.style.display = "none";
    return;
  }
  ghost.style.display = "block";

  const charsPerMin = state.pbWpm * 5;
  const ghostChars = clamp(Math.floor((charsPerMin / 60) * state.elapsedS), 0, state.source.length);

  const info = getCaretTargetRect(ghostChars);
  if (!info) return;

  const wrapRect = info.wrap.getBoundingClientRect();
  const x = info.left - wrapRect.left + info.wrap.scrollLeft;
  const y = info.top - wrapRect.top + info.wrap.scrollTop;

  ghost.style.left = `${Math.round(x)}px`;
  ghost.style.top = `${Math.round(y)}px`;
}

function recordMistake(expectedCh, gotCh) {
  // We track expected char misses (heatmap by expected key).
  if (expectedCh === gotCh) return;
  const k = expectedCh;
  state.mistakes.set(k, (state.mistakes.get(k) || 0) + 1);
}

function onInput() {
  if (state.finished) return;

  const value = $("input").value;
  const src = state.source;
  const clamped = value.slice(0, src.length);
  if (value !== clamped) {
    $("input").value = clamped;
  }

  const prev = state.typed;
  state.typed = clamped;

  if (!state.started && state.typed.length > 0) {
    state.started = true;
    state.startTs = nowMs();
    state.events = [{ t: 0, n: 0 }];
    state.burstMax = 0;
    state.mistakes = new Map();
    startTimers();
  }

  // recompute correct count cheaply
  let correct = 0;
  const limit = Math.min(state.typed.length, src.length);
  for (let i = 0; i < limit; i++) {
    if (state.typed[i] === src[i]) correct++;
  }
  state.correct = correct;

  // record mistake only when user adds a new char
  if (state.started && state.typed.length > prev.length) {
    const i = state.typed.length - 1;
    if (i >= 0 && i < src.length) {
      recordMistake(src[i], state.typed[i]);
      if (state.typed[i] !== src[i] && state.spans[i]) {
        const s = state.spans[i];
        s.classList.remove("shake");
        void s.offsetWidth;
        s.classList.add("shake");
      }
    }
  }

  if (state.started) {
    const t = (nowMs() - state.startTs) / 1000;
    state.events.push({ t, n: state.typed.length });
    updateBurst();
  }

  applyHighlighting();
  moveCaret();
  moveGhostCaret();
  updateStatsUI();

  if (state.typed === state.source && state.started) {
    finishRun();
  }
}

function chartInit() {
  const ctx = $("chart").getContext("2d");
  const chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "WPM",
          data: [],
          borderColor: "#d1d0c5",
          backgroundColor: "rgba(209,208,197,0.10)",
          fill: true,
          tension: 0.35,
          pointRadius: 0,
          borderWidth: 2
        },
      ],
    },
    options: {
      responsive: true,
      animation: false,
      scales: {
        x: {
          ticks: { color: "#646669" },
          grid: { color: "rgba(255,255,255,0.06)" },
        },
        y: {
          ticks: { color: "#646669" },
          grid: { color: "rgba(255,255,255,0.06)" },
          suggestedMin: 0,
          suggestedMax: 120,
        },
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false },
      },
    },
  });
  return chart;
}

let chart = null;

function graphReset() {
  if (!chart) return;
  chart.data.labels = [];
  chart.data.datasets[0].data = [];
  chart.update();
}

function graphTick() {
  if (!state.started || state.finished) return;
  const { wpm } = computeStats();
  const t = Math.max(0, Math.floor(state.elapsedS));

  if (!chart) return;
  chart.data.labels.push(String(t));
  chart.data.datasets[0].data.push(Number(wpm.toFixed(2)));

  // keep last 60 seconds visible
  if (chart.data.labels.length > 60) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
  }
  chart.update();
}

function renderWeaknesses() {
  const el = $("weaknesses");
  if (state.mistakes.size === 0) {
    el.textContent = "No mistakes recorded. Clean run.";
    return;
  }

  const entries = [...state.mistakes.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8);
  const lines = entries.map(([ch, n]) => `- ${fmtChar(ch)}: ${n}`);
  el.textContent = lines.join("\n");
}

function showDashboard() {
  const live = $("liveView");
  const dash = $("dashView");
  live.classList.add("fadeOut");
  setTimeout(() => {
    live.classList.add("hidden");
    dash.classList.remove("hidden");
    dash.classList.remove("fadeOut");
    dash.classList.add("fadeIn");
  }, 220);

  const { wpm, acc } = computeStats();
  $("dashWpm").textContent = wpm.toFixed(1);
  $("dashBurst").textContent = state.burstMax.toFixed(1);
  $("dashAcc").textContent = `${acc.toFixed(1)}%`;
  $("dashTime").textContent = `${state.elapsedS.toFixed(1)}s`;
}

function hideDashboard() {
  const live = $("liveView");
  const dash = $("dashView");
  dash.classList.add("hidden");
  dash.classList.remove("fadeIn");
  live.classList.remove("hidden");
  live.classList.remove("fadeOut");
  live.classList.add("fadeIn");
}

async function finishRun() {
  state.finished = true;
  stopTimers();
  renderWeaknesses();
  showDashboard();

  const { wpm } = computeStats();
  try {
    const res = await apiCall("save_personal_best", wpm);
    if (res && typeof res.personal_best_wpm === "number") {
      state.pbWpm = res.personal_best_wpm;
      updateStatsUI();
    }
  } catch {
    // ignore
  }
}

function startTimers() {
  stopTimers();
  state.tickTimer = setInterval(() => {
    state.elapsedS = (nowMs() - state.startTs) / 1000;
    updateStatsUI();
    moveGhostCaret();
  }, 100);

  state.graph.timer = setInterval(() => {
    if (!state.started || state.finished) return;
    graphTick();
  }, 1000);
}

function stopTimers() {
  if (state.tickTimer) clearInterval(state.tickTimer);
  if (state.graph.timer) clearInterval(state.graph.timer);
  state.tickTimer = null;
  state.graph.timer = null;
}

async function restart() {
  hideDashboard();
  stopTimers();

  state.started = false;
  state.finished = false;
  state.elapsedS = 0;
  state.startTs = 0;
  state.typed = "";
  state.correct = 0;
  state.mistakes = new Map();
  state.events = [{ t: 0, n: 0 }];
  state.burstMax = 0;
  state.lastStats = { wpm: null, acc: null };

  $("input").value = "";
  $("weaknesses").textContent = "No mistakes recorded.";
  graphReset();

  const p = await apiCall("get_paragraph");
  state.source = p.text || "";
  state.spans = buildSourceSpans(state.source);
  applyHighlighting();
  moveCaret();
  moveGhostCaret();
  updateStatsUI();

  $("input").focus();
}

async function init() {
  chart = chartInit();
  try {
    const s = await apiCall("get_initial_state");
    if (s && typeof s.personal_best_wpm === "number") state.pbWpm = s.personal_best_wpm;
  } catch {
    // ignore
  }

  $("btnRestart").addEventListener("click", restart);
  $("btnRestartFromDash").addEventListener("click", restart);
  $("input").addEventListener("input", onInput);
  $("toggleGhost").addEventListener("change", (e) => {
    state.ghostEnabled = !!e.target.checked;
    moveGhostCaret();
  });

  window.addEventListener("resize", () => {
    moveCaret();
    moveGhostCaret();
  });
  $("sourceWrap").addEventListener("scroll", () => {
    moveCaret();
    moveGhostCaret();
  });

  await restart();
}

window.addEventListener("pywebviewready", () => {
  init().catch((e) => {
    console.error(e);
  });
});

