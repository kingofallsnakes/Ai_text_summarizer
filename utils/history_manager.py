# utils/history_manager.py
import json
import os

HISTORY_FILE = "history.json"

def save_summary(text, summary):
    entry = {"text": text, "summary": summary}
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)
