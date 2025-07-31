import json
from datetime import datetime

def load_history():
    try:
        with open("chat_history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("[HISTORY LOAD ERROR]", e)
        return []

def save_history(history):
    with open("chat_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def get_history_by_date(start_date=None, end_date=None):
    try:
        history = load_history()
        filtered = []
        for entry in history:
            timestamp = entry.get("timestamp", "")
            if not timestamp:
                continue
            date_only = timestamp[:10]
            if start_date and end_date:
                if start_date <= date_only <= end_date:
                    filtered.append(entry)
            elif start_date == date_only:
                filtered.append(entry)
        return filtered
    except Exception as e:
        print("[DATE FILTER ERROR]", e)
        return []

def get_history_by_topic(topic):
    try:
        history = load_history()
        topic = topic.lower()
        return [
            entry for entry in history
            if topic in entry.get("user", "").lower() or topic in entry.get("nova", "").lower()
        ]
    except Exception as e:
        print("[TOPIC FILTER ERROR]", e)
        return []

def clear_history_by_topic(topic):
    try:
        history = load_history()
        topic = topic.lower()
        cleaned = [
            entry for entry in history
            if topic not in entry.get("user", "").lower() and topic not in entry.get("nova", "").lower()
        ]
        save_history(cleaned)
        return {"status": "Topic cleared from history"}
    except Exception as e:
        print("[HISTORY CLEAR ERROR]", e)
        return {"error": str(e)}

def summarize_day(date):
    try:
        entries = get_history_by_date(start_date=date, end_date=date)
        if not entries:
            return {"summary": f"No entries for {date}"}
        convo = "\n".join(f"User: {e['user']}\nNova: {e['nova']}" for e in entries)
        # Optional: plug this into Nova’s model_runner or other summarizer
        return {"summary": convo}
    except Exception as e:
        print("[DAY SUMMARY ERROR]", e)
        return {"error": str(e)}