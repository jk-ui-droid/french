#!/usr/bin/env python3
"""Generate index.html with multilingual support for both UI and vocabulary."""

import os
import json

# Load all language CSVs
csv_data = {}
languages = ['en', 'fr', 'de', 'es', 'it', 'pl']

for lang in languages:
    csv_file = 'lang_source/vocab_{}.csv'.format(lang)
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as f:
            csv_data[lang] = f.read()

# Load UI translations
ui_strings = {}
for lang in languages:
    props_file = 'lang_source/ui_{}.properties'.format(lang)
    if os.path.exists(props_file):
        strings = {}
        with open(props_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    strings[key] = value
        ui_strings[lang] = strings

# Convert to JSON for embedding
csv_data_json = json.dumps(csv_data)
ui_strings_json = json.dumps(ui_strings)

HTML_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>French Vocabulary</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --color-primary: #e7b89f;
  --color-primary-dk: #c9977e;
  --color-primary-lt: #fdf5f1;
  --color-bg: #ffffff;
  --color-panel: #fdf8f5;
  --color-text: #32363a;
  --color-text-muted: #6a6d70;
  --color-border: #e8d8cf;
  --color-again: #bb0000;
  --color-hard: #e76500;
  --color-good: #c9977e;
  --color-easy: #2e7d32;
  --color-danger: #bb0000;
  --color-excluded: #89919a;
  --radius: 0.5rem;
  --shadow: 0 2px 8px rgba(0,0,0,0.10);
  --font: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: var(--font); background: var(--color-panel); color: var(--color-text); min-height: 100vh; }
#shellbar { background: var(--color-primary); color: #fff; padding: 0.75rem 1.5rem; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 4px rgba(0,0,0,0.15); position: sticky; top: 0; z-index: 100; }
.app-title { font-size: 1.1rem; font-weight: 700; letter-spacing: 0.02em; }
#lang-selector { background: #f5e6e0; border: 1px solid #e8d8cf; color: var(--color-text); padding: 0.3rem 0.6rem; border-radius: 0.3rem; font-size: 0.8rem; cursor: pointer; font-family: var(--font); }
#lang-selector:hover { background: #f0dcd3; }
#tab-nav { display: flex; gap: 0; }
.tab-btn { background: none; border: none; color: rgba(255,255,255,0.7); font: inherit; font-size: 0.9rem; font-weight: 500; padding: 0.5rem 1rem; cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.15s; }
.tab-btn:hover { color: #fff; }
.tab-btn.active { color: #fff; border-bottom-color: #fff; }
.tab-panel { display: none; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }
.tab-panel.active { display: block; }
#session-counter { text-align: center; color: var(--color-text-muted); font-size: 0.85rem; margin-bottom: 1rem; }
#card { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius); box-shadow: var(--shadow); padding: 2rem; min-height: 200px; }
.card-sentence { font-size: 1.35rem; font-weight: 600; line-height: 1.6; margin-bottom: 1.25rem; }
.card-meta { font-size: 0.95rem; color: var(--color-text-muted); margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between; }
.meta-left { display: flex; align-items: center; gap: 0.3rem; }
.meta-sep { color: var(--color-border); margin: 0 0.3rem; }
.blank-placeholder { color: var(--color-primary); cursor: pointer; border-bottom: 2px dashed var(--color-primary); padding: 0 0.2rem; letter-spacing: -1px; }
.blank-placeholder:hover { background: var(--color-primary-lt); }
.blank-input { font: inherit; font-size: 1.35rem; font-weight: 600; color: var(--color-primary); border: none; border-bottom: 2px dashed var(--color-primary); background: transparent; outline: none; padding: 0; margin: 0; max-width: 300px; -webkit-appearance: none; appearance: none; text-indent: 0; }
.blank-measure { position: absolute; visibility: hidden; white-space: pre; font: inherit; font-size: 1.35rem; font-weight: 600; }
.blank-input:focus { background: transparent; }
.answer-correct { color: var(--color-easy); font-weight: 700; }
.answer-wrong { color: var(--color-again); font-weight: 700; text-decoration: line-through; }
.answer-correct-word { color: var(--color-easy); font-weight: 700; }
.card-answer-hl { color: var(--color-primary); font-weight: 700; text-decoration: underline; text-decoration-color: var(--color-primary-lt); text-underline-offset: 3px; }
.card-tense { display: inline-block; background: var(--color-panel); border: 1px solid var(--color-border); border-radius: 0.25rem; padding: 0.15rem 0.6rem; font-size: 0.8rem; color: var(--color-text-muted); }
.card-divider { border: none; border-top: 1px solid var(--color-border); margin: 1.25rem 0; }
.card-definition { font-size: 0.95rem; line-height: 1.5; margin-bottom: 1rem; }
.card-etymology { font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.4; }
.section-label { font-size: 0.8rem; font-weight: 600; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.3rem; }
#action-bar { display: flex; justify-content: center; align-items: center; gap: 0.75rem; margin-top: 1.5rem; flex-wrap: wrap; }
.btn { border: none; border-radius: var(--radius); padding: 0.6rem 1.4rem; font: inherit; font-size: 0.9rem; font-weight: 600; cursor: pointer; transition: background 0.15s, transform 0.1s; }
.btn:active { transform: scale(0.96); }
.btn-show { background: var(--color-primary); color: #fff; padding: 0.75rem 2rem; font-size: 1rem; }
.btn-show:hover { background: var(--color-primary-dk); }
.btn-exclude { background: none; border: 1px solid var(--color-border); color: var(--color-text-muted); font-size: 0.8rem; padding: 0.4rem 0.8rem; margin-left: auto; }
.btn-exclude:hover { border-color: var(--color-danger); color: var(--color-danger); }
.keyboard-hint { font-size: 0.75rem; color: var(--color-text-muted); margin-top: 0.5rem; width: 100%; text-align: center; }
.empty-state { text-align: center; padding: 3rem 1rem; color: var(--color-text-muted); }
.empty-state p { margin-bottom: 0.5rem; }
.empty-state .emoji { font-size: 2.5rem; margin-bottom: 1rem; }
#stats-counters { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem; }
.stat-tile { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius); padding: 1.25rem; flex: 1; min-width: 140px; text-align: center; box-shadow: var(--shadow); }
.stat-tile .label { font-size: 0.8rem; color: var(--color-text-muted); margin-bottom: 0.5rem; }
.stat-tile .number { font-size: 1.8rem; font-weight: 700; color: var(--color-primary); }
#streak-display { text-align: center; margin-bottom: 1.5rem; font-size: 1.1rem; }
.streak-count { font-weight: 700; color: var(--color-primary); }
.section-title { font-size: 1rem; font-weight: 600; margin-bottom: 0.75rem; }
#forecast-toggle { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
.toggle-btn { background: var(--color-panel); border: 1px solid var(--color-border); border-radius: var(--radius); padding: 0.3rem 0.8rem; font: inherit; font-size: 0.8rem; cursor: pointer; }
.toggle-btn.active { background: var(--color-primary); color: #fff; border-color: var(--color-primary); }
#forecast-chart { display: flex; align-items: flex-end; gap: 3px; height: 140px; background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius); padding: 1rem; margin-bottom: 2rem; }
.bar-col { display: flex; flex-direction: column; align-items: center; flex: 1; height: 100%; justify-content: flex-end; }
.bar-fill { background: var(--color-primary); border-radius: 2px 2px 0 0; width: 70%; min-width: 8px; transition: height 0.3s; }
.bar-label { font-size: 0.6rem; color: var(--color-text-muted); margin-top: 4px; white-space: nowrap; }
.bar-count { font-size: 0.65rem; color: var(--color-text); margin-bottom: 2px; }
#word-list-section { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius); padding: 1rem; box-shadow: var(--shadow); }
#word-search { width: 100%; padding: 0.5rem 0.75rem; border: 1px solid var(--color-border); border-radius: var(--radius); font: inherit; font-size: 0.9rem; margin-bottom: 0.75rem; }
#word-search:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 2px var(--color-primary-lt); }
#word-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
#word-table th, #word-table td { padding: 0.5rem 0.6rem; text-align: left; border-bottom: 1px solid var(--color-border); }
#word-table th { background: var(--color-panel); font-weight: 600; position: sticky; top: 0; cursor: help; }
#word-table-wrap { max-height: 400px; overflow-y: auto; }
.status-badge { display: inline-block; border-radius: 0.75rem; padding: 0.15rem 0.5rem; font-size: 0.7rem; font-weight: 600; }
.status-new { background: #e8f4fb; color: #0a6ed1; }
.status-learning { background: #fff3e0; color: #e65c00; }
.status-review { background: #e8f5e9; color: #1b6b2a; }
.status-mature { background: #ede7f6; color: #4527a0; }
.status-excluded { background: #eceef0; color: #89919a; }
.btn-reactivate { background: none; border: 1px solid var(--color-primary); color: var(--color-primary); border-radius: var(--radius); padding: 0.2rem 0.5rem; font-size: 0.7rem; cursor: pointer; }
.btn-reactivate:hover { background: var(--color-primary-lt); }
.row-excluded { opacity: 0.5; }
.correct-msg { color: var(--color-easy); font-size: 1.2rem; font-weight: 700; }
.char-bar { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.75rem; justify-content: center; }
.char-btn { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: 4px; padding: 0.3rem 0.55rem; font: inherit; font-size: 1rem; cursor: pointer; line-height: 1; min-width: 2rem; text-align: center; }
.char-btn:hover { border-color: var(--color-primary); color: var(--color-primary); background: var(--color-primary-lt); }
.settings-card { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: var(--radius); padding: 1.5rem; box-shadow: var(--shadow); margin-bottom: 1.5rem; }
.settings-card h3 { font-size: 1rem; margin-bottom: 1rem; }
.settings-card label { font-size: 0.9rem; font-weight: 500; display: block; margin-bottom: 0.5rem; }
#slider-row { display: flex; align-items: center; gap: 1rem; }
#new-cards-slider { flex: 1; accent-color: var(--color-primary); }
#slider-value { font-size: 1.2rem; font-weight: 700; min-width: 2.5rem; text-align: center; }
.danger-link { color: var(--color-danger); font-weight: 600; text-decoration: none; font-size: 0.9rem; }
.danger-link:hover { text-decoration: underline; }
#avalanche-warning { margin-top: 0.75rem; }
.export-import-row { display: flex; gap: 1rem; margin-top: 1rem; }
.btn-secondary { background: var(--color-panel); border: 1px solid var(--color-border); border-radius: var(--radius); padding: 0.5rem 1.2rem; font: inherit; font-size: 0.85rem; font-weight: 500; cursor: pointer; }
.btn-secondary:hover { border-color: var(--color-primary); color: var(--color-primary); }
#modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 200; }
#modal-overlay[hidden] { display: none; }
#modal-box { background: #fff; border-radius: var(--radius); padding: 2rem; max-width: 500px; width: 90%; box-shadow: 0 8px 32px rgba(0,0,0,0.2); }
#modal-box h2 { font-size: 1.1rem; margin-bottom: 1rem; }
#modal-box p { font-size: 0.9rem; line-height: 1.5; margin-bottom: 1rem; color: var(--color-text-muted); }
#modal-close { background: var(--color-primary); color: #fff; border: none; border-radius: var(--radius); padding: 0.5rem 1.5rem; font: inherit; font-weight: 600; cursor: pointer; }
</style>
</head>
<body>

<header id="shellbar">
  <span class="app-title" data-i18n="app.title">French Vocabulary</span>
  <nav id="tab-nav">
    <button class="tab-btn active" data-tab="study" data-i18n="tab.study">Study</button>
    <button class="tab-btn" data-tab="stats" data-i18n="tab.stats">Statistics</button>
    <button class="tab-btn" data-tab="settings" data-i18n="tab.settings">Settings</button>
  </nav>
  <select id="lang-selector">
    <option value="en">English</option>
    <option value="fr">Français</option>
    <option value="de">Deutsch</option>
    <option value="es">Español</option>
    <option value="it">Italiano</option>
    <option value="pl">Polski</option>
  </select>
</header>

<main id="tab-study" class="tab-panel active">
  <div id="session-counter"></div>
  <div id="card"></div>
  <div id="action-bar"></div>
</main>

<main id="tab-stats" class="tab-panel">
  <div id="stats-counters"></div>
  <div id="streak-display"></div>
  <div class="section-title" data-i18n="stats.title.forecast">Review forecast</div>
  <div id="forecast-toggle">
    <button class="toggle-btn active" data-days="7" data-i18n="forecast.days.7">7 days</button>
    <button class="toggle-btn" data-days="30" data-i18n="forecast.days.30">30 days</button>
  </div>
  <div id="forecast-chart"></div>
  <div id="word-list-section">
    <input id="word-search" type="search" data-i18n-placeholder="word.search.placeholder" placeholder="Filter by word...">
    <div id="word-table-wrap">
      <table id="word-table">
        <thead><tr><th data-i18n="table.header.word" data-i18n-title="tooltip.col.word" title="The French word or phrase">Word</th><th data-i18n="table.header.tense" data-i18n-title="tooltip.col.tense" title="Grammatical tense used in the sentence">Tense</th><th data-i18n="table.header.interval" data-i18n-title="tooltip.col.interval" title="Days until next review">Interval</th><th data-i18n="table.header.ease" data-i18n-title="tooltip.col.ease" title="Difficulty factor (2.5 = normal, lower = harder)">Ease</th><th data-i18n="table.header.due" data-i18n-title="tooltip.col.due" title="Date when card is next due for review">Due</th><th data-i18n="table.header.status" data-i18n-title="tooltip.col.status" title="Current learning status of the card">Status</th><th></th></tr></thead>
        <tbody id="word-table-body"></tbody>
      </table>
    </div>
  </div>
</main>

<main id="tab-settings" class="tab-panel">
  <div class="settings-card">
    <h3 data-i18n="settings.new.cards">New cards per day</h3>
    <div id="slider-row">
      <input type="range" id="new-cards-slider" min="1" max="100" value="20">
      <span id="slider-value">20</span>
    </div>
    <p id="avalanche-warning" hidden>
      <a href="#" id="avalanche-link" class="danger-link" data-i18n="modal.avalanche.title">Review avalanche</a>
    </p>
  </div>
  <div class="settings-card">
    <h3 data-i18n="settings.data">Data</h3>
    <div class="export-import-row">
      <button class="btn-secondary" id="btn-export" data-i18n="btn.export">Export progress</button>
      <button class="btn-secondary" id="btn-import" data-i18n="btn.import">Import progress</button>
      <input type="file" id="import-file" accept=".json" hidden>
    </div>
  </div>
</main>

<div id="modal-overlay" hidden>
  <div id="modal-box">
    <h2 data-i18n="modal.avalanche.title">Review avalanche</h2>
    <p data-i18n="modal.avalanche.text">When you introduce unlimited new cards, each card reviewed today generates future reviews. In a few days, you could find yourself with hundreds of cards due on the same day.</p>
    <p data-i18n="modal.avalanche.text2">This phenomenon is called a "review avalanche". It can be discouraging and lead to abandoning learning.</p>
    <p data-i18n="modal.avalanche.text3">It is recommended to start with 10 to 20 new cards per day to maintain a manageable review load in the long term.</p>
    <button id="modal-close" data-i18n="modal.close">Close</button>
  </div>
</div>

<script>
const ALL_CSV_DATA = ''' + csv_data_json + ''';
const UI_STRINGS = ''' + ui_strings_json + ''';
let CurrentUILang = 'en';
let CurrentCardLang = 'en';
let CARDS = [];

function t(key, defaultText = key) {
  const strings = UI_STRINGS[CurrentUILang] || {};
  return strings[key] || UI_STRINGS['en'][key] || defaultText;
}

function updateUIText() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    el.textContent = t(key, el.textContent);
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    el.placeholder = t(key, el.placeholder);
  });
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    const key = el.getAttribute('data-i18n-title');
    el.title = t(key, el.title);
  });
}

document.getElementById('lang-selector').addEventListener('change', e => {
  CurrentUILang = e.target.value;
  CurrentCardLang = e.target.value;
  localStorage.setItem('uiLang', CurrentUILang);
  updateUIText();
  // Reload cards with new language
  const csvText = ALL_CSV_DATA[CurrentCardLang] || ALL_CSV_DATA['en'];
  CARDS = Object.freeze(parseCSV(csvText));
  // Re-render current view
  if (document.getElementById('tab-study').classList.contains('active')) {
    showStudyTab();
  } else if (document.getElementById('tab-stats').classList.contains('active')) {
    renderStats();
  }
});

window.addEventListener('DOMContentLoaded', () => {
  const saved = localStorage.getItem('uiLang');
  if (saved && UI_STRINGS[saved]) {
    CurrentUILang = saved;
    CurrentCardLang = saved;
    document.getElementById('lang-selector').value = saved;
  }
  updateUIText();
  const csvText = ALL_CSV_DATA[CurrentCardLang] || ALL_CSV_DATA['en'];
  CARDS = Object.freeze(parseCSV(csvText));
});
</script>

<script>
'''

HTML_SCRIPT = '''
// ===== CSV PARSER =====
function parseCSV(text) {
  const rows = [];
  let i = 0;
  const len = text.length;
  function parseField() {
    if (text[i] === '"') {
      i++;
      let val = '';
      while (i < len) {
        if (text[i] === '"') {
          if (text[i+1] === '"') { val += '"'; i += 2; }
          else { i++; break; }
        } else { val += text[i++]; }
      }
      return val;
    } else {
      let start = i;
      while (i < len && text[i] !== ',' && text[i] !== '\\n' && text[i] !== '\\r') i++;
      return text.slice(start, i);
    }
  }
  function parseRow() {
    const fields = [];
    while (i < len && text[i] !== '\\n' && text[i] !== '\\r') {
      fields.push(parseField());
      if (text[i] === ',') i++;
    }
    if (text[i] === '\\r') i++;
    if (text[i] === '\\n') i++;
    return fields;
  }
  const headers = parseRow();
  while (i < len) {
    if (text[i] === '\\r' || text[i] === '\\n') { i++; continue; }
    const fields = parseRow();
    if (fields.length === headers.length) {
      const obj = {};
      headers.forEach((h, idx) => { obj[h] = fields[idx]; });
      obj.sentence = obj.sentence.replace(/_{3,}/g, '_____');
      rows.push(obj);
    }
  }
  return rows;
}

// ===== STORAGE =====
const STORAGE_KEY = 'fr_vocab_app';
const DEFAULT_STATE = {
  cards: {},
  settings: { newCardsPerDay: 20 },
  stats: { streak: 0, lastStudyDate: null, todayNewCount: 0, sessionHistory: [] }
};

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return JSON.parse(JSON.stringify(DEFAULT_STATE));
    const saved = JSON.parse(raw);
    return {
      cards: saved.cards || {},
      settings: { ...DEFAULT_STATE.settings, ...(saved.settings || {}) },
      stats: { ...DEFAULT_STATE.stats, ...(saved.stats || {}) }
    };
  } catch(e) { return JSON.parse(JSON.stringify(DEFAULT_STATE)); }
}

function saveState() {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(AppState)); } catch(e) {}
}

function persistCardUpdate(cardIdx, cardRecord) {
  AppState.cards[String(cardIdx)] = cardRecord;
  saveState();
}

function exportProgress() {
  const blob = new Blob([JSON.stringify(AppState, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'vocab_progress_' + getTodayDateString() + '.json';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function importProgress(file) {
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const data = JSON.parse(e.target.result);
      if (!data.cards || !data.settings || !data.stats) {
        alert(t('alert.invalid.file', 'Invalid file: incorrect structure.'));
        return;
      }
      if (!confirm(t('confirm.import', 'This will replace your current progress. Continue?'))) return;
      AppState = data;
      saveState();
      location.reload();
    } catch(err) { alert(t('alert.read.error', 'Error reading file.')); }
  };
  reader.readAsText(file);
}

// ===== SM-2 ENGINE =====
function getTodayDateString() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return y + '-' + m + '-' + day;
}

function addDays(dateStr, n) {
  const parts = dateStr.split('-');
  const d = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
  d.setDate(d.getDate() + n);
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return y + '-' + m + '-' + day;
}

const TODAY = getTodayDateString();

function defaultCardRecord() {
  return { interval: 0, easeFactor: 2.5, repetitions: 0, dueDate: TODAY, lapses: 0, excluded: false };
}

function scheduleCard(record, rating) {
  let { interval, easeFactor, repetitions, lapses, excluded } = record;
  if (rating === 1) {
    repetitions = 0;
    interval = 1;
    easeFactor = Math.max(1.3, easeFactor - 0.2);
    lapses++;
    return { newRecord: { interval, easeFactor, repetitions, dueDate: addDays(TODAY, 1), lapses, excluded: false }, requeue: true };
  }
  if (repetitions === 0) { interval = 1; repetitions = 1; }
  else if (repetitions === 1) { interval = 4; repetitions = 2; }
  else {
    if (rating === 2) { interval = Math.round(interval * 1.2); easeFactor = Math.max(1.3, easeFactor - 0.15); }
    else if (rating === 3) { interval = Math.round(interval * easeFactor); }
    else { interval = Math.round(interval * easeFactor * 1.3); easeFactor = Math.min(easeFactor + 0.15, 9.9); }
    repetitions++;
  }
  return { newRecord: { interval, easeFactor, repetitions, dueDate: addDays(TODAY, interval), lapses, excluded: false }, requeue: false };
}

// ===== QUEUE =====
let SessionQueue = [];
let CurrentIdx = 0;
let CardStart = null;
let WaitingForNext = false;

function buildQueue() {
  const settings = AppState.settings;
  const stats = AppState.stats;
  if (stats.lastStudyDate !== TODAY) { stats.todayNewCount = 0; }

  const dueReviews = [];
  const newCards = [];

  CARDS.forEach((card, idx) => {
    const rec = AppState.cards[String(idx)];
    if (rec && rec.excluded) return;
    if (!rec || rec.repetitions === 0) { newCards.push(idx); }
    else if (rec.dueDate <= TODAY) { dueReviews.push(idx); }
  });

  dueReviews.sort((a, b) => {
    const ra = AppState.cards[String(a)];
    const rb = AppState.cards[String(b)];
    return (ra.dueDate || '').localeCompare(rb.dueDate || '');
  });

  const maxNew = settings.newCardsPerDay >= 100
    ? newCards.length
    : Math.max(0, settings.newCardsPerDay - stats.todayNewCount);

  SessionQueue = [...dueReviews, ...newCards.slice(0, maxNew)];
  CurrentIdx = 0;
}

function currentCard() {
  if (CurrentIdx >= SessionQueue.length) return null;
  return { idx: SessionQueue[CurrentIdx], data: CARDS[SessionQueue[CurrentIdx]] };
}

function advanceQueue(requeue) {
  if (requeue) { SessionQueue.push(SessionQueue[CurrentIdx]); }
  CurrentIdx++;
}

// ===== STUDY VIEW =====
function escHtml(str) {
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function updateProgress() {
  const total = new Set(SessionQueue).size;
  const done = new Set(SessionQueue.slice(0, CurrentIdx)).size;
  document.getElementById('session-counter').textContent = done + ' / ' + total + ' ' + t('session.counter', 'cards').split('{done} / {total} ')[1];
}

function showStudyTab() {
  buildQueue();
  const card = currentCard();
  if (!card) { renderEmptyState(); return; }
  renderFront(card);
}

function renderFront(card) {
  const { data } = card;
  const sentenceHTML = data.sentence.replace('_____', '<span class="blank-placeholder" id="blank-target">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>');
  document.getElementById('card').innerHTML =
    '<div class="card-meta"><span class="meta-left">' + escHtml(data.user_language) + ' <span class="meta-sep">|</span> ' + escHtml(data.tense) + '</span><button class="btn btn-exclude" id="btn-exclude">' + t('btn.exclude', 'Exclude') + '</button></div>' +
    '<p class="card-sentence" id="sentence-area">' + sentenceHTML + '</p>';
  document.getElementById('action-bar').innerHTML = '';
  CardStart = Date.now();
  updateProgress();
  showCharBar();
  activateInput();
}

function activateInput() {
  const blank = document.getElementById('blank-target');
  if (!blank || blank.tagName === 'INPUT') return;
  const card = currentCard();
  if (!card) return;
  const input = document.createElement('input');
  input.type = 'text';
  input.className = 'blank-input';
  input.id = 'answer-input';
  input.setAttribute('autocomplete', 'off');
  input.setAttribute('autocorrect', 'off');
  input.setAttribute('autocapitalize', 'off');
  input.setAttribute('spellcheck', 'false');
  const measure = document.createElement('span');
  measure.className = 'blank-measure';
  measure.id = 'blank-measure';
  document.body.appendChild(measure);
  function resizeInput() {
    measure.textContent = input.value || 'mmmm';
    var w = measure.offsetWidth + 10;
    measure.textContent = 'mmmm';
    var minW = measure.offsetWidth + 10;
    input.style.width = Math.max(w, minW) + 'px';
  }
  blank.replaceWith(input);
  resizeInput();
  input.focus();
  input.addEventListener('input', resizeInput);
}

function showCharBar() {
  if (document.getElementById('char-bar')) return;
  const chars = ['é','è','ê','ë','à','â','ç','ù','û','ü','ô','î','ï','œ','æ','ÿ'];
  const bar = document.createElement('div');
  bar.className = 'char-bar';
  bar.id = 'char-bar';
  chars.forEach(ch => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'char-btn';
    btn.textContent = ch;
    btn.addEventListener('mousedown', e => {
      e.preventDefault();
      insertChar(ch);
    });
    bar.appendChild(btn);
  });
  const sentenceArea = document.getElementById('sentence-area');
  if (sentenceArea) sentenceArea.after(bar);
}

function insertChar(ch) {
  const input = document.getElementById('answer-input');
  if (!input || input.disabled) return;
  const start = input.selectionStart;
  const end = input.selectionEnd;
  const val = input.value;
  input.value = val.slice(0, start) + ch + val.slice(end);
  input.selectionStart = input.selectionEnd = start + ch.length;
  input.focus();
  const measure = document.getElementById('blank-measure');
  if (measure) { measure.textContent = input.value || 'mmmm'; var w = measure.offsetWidth + 10; measure.textContent = 'mmmm'; var minW = measure.offsetWidth + 10; input.style.width = Math.max(w, minW) + 'px'; }
}

function normalizeAnswer(str) {
  return str.trim().toLowerCase()
    .replace(/[\\u2019\\u2018]/g, "'")
    .replace(/\\s+/g, ' ');
}

function evaluateAnswer() {
  const input = document.getElementById('answer-input');
  if (!input) return;
  const card = currentCard();
  if (!card) return;
  const userAnswer = normalizeAnswer(input.value);
  const correctAnswer = normalizeAnswer(card.data.answer);
  const isCorrect = userAnswer === correctAnswer;

  if (isCorrect) {
    input.disabled = true;
    input.classList.add('answer-correct');
    input.value = card.data.answer;
    const charBar = document.getElementById('char-bar');
    if (charBar) charBar.hidden = true;
    document.getElementById('action-bar').innerHTML =
      '<div class="correct-msg">' + t('msg.correct', 'Correct!') + '</div><div style="width:100%;display:flex;justify-content:center;"><button class="btn btn-show" id="btn-correct-continue">' + t('btn.continue', 'Continue') + '</button></div>';
    WaitingForNext = true;
  } else {
    renderBack(card, input.value.trim());
  }
}

function renderBack(card, wrongAnswer) {
  const { data } = card;
  const answerSpan = wrongAnswer
    ? '<span class="answer-wrong">' + escHtml(wrongAnswer) + '</span><span class="answer-correct-word">/' + escHtml(data.answer) + '</span>'
    : '<span class="card-answer-hl">' + escHtml(data.answer) + '</span>';
  const sentenceHTML = data.sentence.replace('_____', answerSpan);
  document.getElementById('card').innerHTML =
    '<div class="card-meta"><span class="meta-left">' + escHtml(data.user_language) + ' <span class="meta-sep">|</span> ' + escHtml(data.tense) + '</span><button class="btn btn-exclude" id="btn-exclude">' + t('btn.exclude', 'Exclude') + '</button></div>' +
    '<p class="card-sentence">' + sentenceHTML + '</p>' +
    '<hr class="card-divider">' +
    '<p class="section-label">' + t('section.definition', 'Definition') + '</p>' +
    '<p class="card-definition">' + escHtml(data.definition_fr) + '</p>' +
    '<p class="section-label">' + t('section.etymology', 'Etymology') + '</p>' +
    '<p class="card-etymology">' + escHtml(data.etymology) + '</p>';
  document.getElementById('action-bar').innerHTML =
    '<button class="btn btn-show" id="btn-continue">' + t('btn.continue', 'Continue') + '</button>';
}

function handleAnswer(correct) {
  const card = currentCard();
  if (!card) return;
  const isNew = !AppState.cards[String(card.idx)] || AppState.cards[String(card.idx)].repetitions === 0;
  const existing = AppState.cards[String(card.idx)] || defaultCardRecord();
  const rating = correct ? 3 : 1;
  const { newRecord, requeue } = scheduleCard(existing, rating);
  if (isNew && correct) { AppState.stats.todayNewCount++; }
  const elapsed = (Date.now() - CardStart) / 1000;
  updateAvgTime(elapsed);
  persistCardUpdate(card.idx, newRecord);
  advanceQueue(requeue);
  const next = currentCard();
  if (!next) { finishSession(); } else { renderFront(next); }
}

function handleExclude() {
  const card = currentCard();
  if (!card) return;
  if (!confirm(t('confirm.exclude', 'This card will be permanently excluded from your reviews. You can reactivate it in the Statistics tab.\\n\\nContinue?'))) return;
  const existing = AppState.cards[String(card.idx)] || defaultCardRecord();
  existing.excluded = true;
  persistCardUpdate(card.idx, existing);
  advanceQueue(false);
  const next = currentCard();
  if (!next) { finishSession(); } else { renderFront(next); }
}

function finishSession() {
  if (AppState.stats.todayNewCount > 0 || Object.values(AppState.cards).some(r => r.repetitions > 0 && r.dueDate < TODAY)) {
    updateStreak();
  }
  saveState();
  renderEmptyState();
}

function renderEmptyState() {
  document.getElementById('card').innerHTML =
    '<div class="empty-state"><div class="emoji">🎉</div>' +
    '<p><strong>' + t('empty.title', 'Congratulations!') + '</strong></p>' +
    '<p>' + t('empty.message', 'All cards for today are finished.') + '</p>' +
    '<p>' + t('empty.next', 'Come back tomorrow for new reviews.') + '</p></div>';
  document.getElementById('action-bar').innerHTML = '';
  document.getElementById('session-counter').textContent = '';
}

function updateStreak() {
  const stats = AppState.stats;
  const yesterday = addDays(TODAY, -1);
  if (stats.lastStudyDate === TODAY) return;
  if (stats.lastStudyDate === yesterday) { stats.streak++; }
  else { stats.streak = 1; }
  stats.lastStudyDate = TODAY;
}

function updateAvgTime(elapsed) {
  const capped = Math.min(elapsed, 120);
  const stats = AppState.stats;
  const entry = stats.sessionHistory.find(e => e.date === TODAY);
  if (entry) {
    entry.avgTime = (entry.avgTime * entry.reviewed + capped) / (entry.reviewed + 1);
    entry.reviewed++;
  } else {
    stats.sessionHistory.push({ date: TODAY, reviewed: 1, avgTime: capped });
    if (stats.sessionHistory.length > 90) stats.sessionHistory = stats.sessionHistory.slice(-90);
  }
}

// ===== STATS VIEW =====
function renderStats() {
  const cardStates = AppState.cards;
  let countNew = 0, countLearning = 0, countReview = 0, countStarted = 0;
  CARDS.forEach((_, idx) => {
    const rec = cardStates[String(idx)];
    if (rec && rec.excluded) return;
    if (!rec || rec.repetitions === 0) countNew++;
    else { countStarted++; if (rec.interval <= 1) countLearning++; else if (rec.dueDate <= TODAY) countReview++; }
  });

  const maxNew = AppState.settings.newCardsPerDay >= 100
    ? countNew
    : Math.max(0, AppState.settings.newCardsPerDay - AppState.stats.todayNewCount);
  const displayNew = Math.min(countNew, maxNew);

  const history = AppState.stats.sessionHistory;
  const avgTime = history.length > 0
    ? history.slice(-5).reduce((a, b) => a + b.avgTime, 0) / Math.min(5, history.length)
    : 10;
  const totalDue = displayNew + countLearning + countReview;
  const estMinutes = Math.max(1, Math.round((totalDue * avgTime) / 60));

  document.getElementById('stats-counters').innerHTML =
    '<div class="stat-tile" title="' + t('tooltip.started', 'Total cards started out of all available') + '"><div class="label">' + t('stats.label.started', 'Started') + '</div><div class="number">' + countStarted + ' / ' + CARDS.length + '</div></div>' +
    '<div class="stat-tile" title="' + t('tooltip.new', 'New cards available today based on your daily limit') + '"><div class="label">' + t('stats.label.new', 'New') + '</div><div class="number">' + displayNew + '</div></div>' +
    '<div class="stat-tile" title="' + t('tooltip.learning', 'Cards in the learning phase') + '"><div class="label">' + t('stats.label.learning', 'Learning') + '</div><div class="number">' + countLearning + '</div></div>' +
    '<div class="stat-tile" title="' + t('tooltip.review', 'Cards due for review today') + '"><div class="label">' + t('stats.label.review', 'To review') + '</div><div class="number">' + countReview + '</div></div>' +
    '<div class="stat-tile" title="' + t('tooltip.time', 'Estimated time to complete today') + '"><div class="label">' + t('stats.label.time', 'Estimated time') + '</div><div class="number">' + (totalDue > 0 ? estMinutes + ' min' : '0 min') + '</div></div>';

  document.getElementById('streak-display').innerHTML =
    '<span class="streak-count">' + AppState.stats.streak + '</span> ' + t('streak.label', 'day streak').replace('{number}', AppState.stats.streak).replace('{plural}', AppState.stats.streak !== 1 ? 's' : '');

  renderForecastChart(7);
  renderWordList('');
}

function renderForecastChart(days) {
  const data = [];
  for (let i = 0; i < days; i++) {
    const target = addDays(TODAY, i);
    let count = 0;
    Object.entries(AppState.cards).forEach(([idx, rec]) => {
      if (rec.excluded) return;
      if (rec.repetitions > 0 && rec.dueDate === target) count++;
    });
    const label = i === 0 ? t('forecast.today', 'Today') : new Date(target + 'T12:00:00').toLocaleDateString('en-US', { weekday: 'short' });
    data.push({ label, count });
  }
  const maxCount = Math.max(...data.map(d => d.count), 1);
  document.getElementById('forecast-chart').innerHTML = data.map(d =>
    '<div class="bar-col">' +
    '<div class="bar-count">' + (d.count || '') + '</div>' +
    '<div class="bar-fill" style="height:' + Math.max(2, Math.round((d.count / maxCount) * 90)) + 'px"></div>' +
    '<div class="bar-label">' + d.label + '</div></div>'
  ).join('');
}

function renderWordList(filter) {
  const lower = filter.toLowerCase();
  const rows = CARDS.map((card, idx) => ({ card, idx, rec: AppState.cards[String(idx)] }))
    .filter(({ card }) => !lower || card.word.toLowerCase().includes(lower));
  const html = rows.map(({ card, idx, rec }) => {
    const interval = rec ? rec.interval : 0;
    const ease = rec ? rec.easeFactor : 2.5;
    const dueDate = rec && rec.repetitions > 0 ? rec.dueDate : '–';
    const excluded = rec && rec.excluded;
    const status = getCardStatus(rec);
    const statusCls = 'status-' + status.toLowerCase();
    const rowCls = excluded ? ' class="row-excluded"' : '';
    const actionBtn = excluded ? '<button class="btn-reactivate" data-idx="' + idx + '">' + t('btn.reactivate', 'Reactivate') + '</button>' : '';
    return '<tr' + rowCls + '><td>' + escHtml(card.word) + '</td><td>' + escHtml(card.tense) +
      '</td><td>' + (interval > 0 ? interval + 'd' : '–') + '</td><td>' + ease.toFixed(2) +
      '</td><td>' + dueDate + '</td><td><span class="status-badge ' + statusCls + '">' + t('status.' + status.toLowerCase(), status) +
      '</span></td><td>' + actionBtn + '</td></tr>';
  }).join('');
  document.getElementById('word-table-body').innerHTML = html;
}

function getCardStatus(rec) {
  if (rec && rec.excluded) return 'Excluded';
  if (!rec || rec.repetitions === 0) return 'New';
  if (rec.interval <= 1) return 'Learning';
  if (rec.interval >= 21) return 'Mature';
  return 'Review';
}

function handleReactivate(idx) {
  const rec = AppState.cards[String(idx)];
  if (rec) { rec.excluded = false; persistCardUpdate(idx, rec); }
  renderWordList(document.getElementById('word-search').value);
}

// ===== SETTINGS =====
function initSettings() {
  const slider = document.getElementById('new-cards-slider');
  const display = document.getElementById('slider-value');
  const warning = document.getElementById('avalanche-warning');
  slider.value = AppState.settings.newCardsPerDay;
  updateSliderDisplay();

  function updateSliderDisplay() {
    const val = parseInt(slider.value, 10);
    if (val >= 100) {
      display.textContent = '∞';
      display.style.color = 'var(--color-danger)';
      warning.hidden = false;
    } else {
      display.textContent = val;
      display.style.color = 'var(--color-text)';
      warning.hidden = true;
    }
  }

  slider.addEventListener('input', () => {
    AppState.settings.newCardsPerDay = parseInt(slider.value, 10);
    saveState();
    updateSliderDisplay();
  });
}

// ===== BOOTSTRAP =====
let AppState;

document.addEventListener('DOMContentLoaded', () => {
  // Restore language preference
  const saved = localStorage.getItem('uiLang');
  if (saved && UI_STRINGS[saved]) {
    CurrentUILang = saved;
    CurrentCardLang = saved;
    document.getElementById('lang-selector').value = saved;
    updateUIText();
  }

  // Ensure cards are loaded with correct language
  if (!CARDS || CARDS.length === 0) {
    const csvText = ALL_CSV_DATA[CurrentCardLang] || ALL_CSV_DATA['en'];
    CARDS = Object.freeze(parseCSV(csvText));
  }

  AppState = loadState();
  if (AppState.stats.lastStudyDate !== TODAY) { AppState.stats.todayNewCount = 0; }

  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
  });

  document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderForecastChart(parseInt(btn.dataset.days, 10));
    });
  });

  document.getElementById('word-search').addEventListener('input', e => renderWordList(e.target.value));

  document.getElementById('word-table-body').addEventListener('click', e => {
    const btn = e.target.closest('.btn-reactivate');
    if (btn) handleReactivate(parseInt(btn.dataset.idx, 10));
  });

  showStudyTab();

  document.addEventListener('keydown', e => {
    const studyActive = document.getElementById('tab-study').classList.contains('active');
    if (!studyActive) return;
    const input = document.getElementById('answer-input');
    const backVisible = document.querySelector('.card-answer-hl') !== null;
    if (WaitingForNext && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault();
      WaitingForNext = false;
      handleAnswer(true);
      return;
    }
    if (input && !input.disabled && e.key === 'Enter') {
      e.preventDefault();
      evaluateAnswer();
      return;
    }
    if (!input && !backVisible && !WaitingForNext && (e.key === ' ' || e.key === 'Enter')) {
      e.preventDefault();
      activateInput();
      return;
    }
    if (backVisible && (e.key === ' ' || e.key === 'Enter')) {
      e.preventDefault();
      handleAnswer(false);
    }
  });

  document.getElementById('action-bar').addEventListener('click', e => {
    if (e.target.id === 'btn-continue' || e.target.closest('#btn-continue')) { handleAnswer(false); return; }
    if (e.target.id === 'btn-correct-continue' || e.target.closest('#btn-correct-continue')) { WaitingForNext = false; handleAnswer(true); return; }
  });

  document.getElementById('card').addEventListener('click', e => {
    if (e.target.id === 'blank-target' || e.target.closest('#blank-target')) {
      activateInput();
      return;
    }
    if (e.target.id === 'btn-exclude' || e.target.closest('#btn-exclude')) {
      handleExclude();
      return;
    }
  });

  document.getElementById('avalanche-link').addEventListener('click', e => {
    e.preventDefault();
    document.getElementById('modal-overlay').hidden = false;
  });
  document.getElementById('modal-close').addEventListener('click', () => {
    document.getElementById('modal-overlay').hidden = true;
  });
  document.getElementById('modal-overlay').addEventListener('click', e => {
    if (e.target.id === 'modal-overlay') e.target.hidden = true;
  });

  document.getElementById('btn-export').addEventListener('click', exportProgress);
  document.getElementById('btn-import').addEventListener('click', () => document.getElementById('import-file').click());
  document.getElementById('import-file').addEventListener('change', e => {
    if (e.target.files[0]) importProgress(e.target.files[0]);
    e.target.value = '';
  });

  initSettings();

  switchTab('study');
});

function switchTab(name) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
  document.querySelector('[data-tab="' + name + '"]').classList.add('active');
  if (name === 'study') showStudyTab();
  if (name === 'stats') renderStats();
}
'''

HTML_FOOT = '''</script>
</body>
</html>'''

# Assemble full HTML
full_html = HTML_HEAD + HTML_SCRIPT + HTML_FOOT

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(full_html)

size = os.path.getsize('index.html')
print('Created index.html: {:,} bytes ({:.0f} KB)'.format(size, size/1024))
print('Embedded: 6 language vocabularies')
print('Support: English, French, German, Spanish, Italian, Polish')
print('Feature: Vocabulary switches with UI language selection')
