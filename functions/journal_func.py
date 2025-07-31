import json
import os
from datetime import datetime
from functions.model_runner import run_model
from functions.memory_func import save_to_memory

def save_to_journal(entry):
    try:
        if not os.path.exists("journal.json"):
            journal = []
        else:
            with open("journal.json", "r", encoding="utf-8") as f:
                journal = json.load(f)
                if not isinstance(journal, list):
                    raise ValueError("journal.json must be a list")

        journal.append(entry)
        with open("journal.json", "w", encoding="utf-8") as f:
            json.dump(journal, f, indent=2)

        # Route entry to structured memory
        route_to_memory(entry)

    except Exception as e:
        print("[JOURNAL SAVE ERROR]", e)

def view_journal():
    try:
        with open("journal.json", "r", encoding="utf-8") as f:
            journal = json.load(f)
            return journal if isinstance(journal, list) else []
    except Exception as e:
        print("[VIEW JOURNAL ERROR]", e)
        return []

def summarize_journal():
    try:
        journal = view_journal()
        if not isinstance(journal, list) or len(journal) < 2:
            return {"summary": "Not enough entries to summarize just yet."}

        convo_text = "\n".join(f"User: {e['user']}\nNova: {e['nova']}" for e in journal[-10:])
        summary_prompt = f"Summarize the following conversation between Franz and Nova:\n{convo_text}\nSummary:"
        summary, stderr = run_model(summary_prompt)
        if stderr:
            print("[SUMMARY STDERR]", stderr)

        return {"summary": summary or "Something went blank—try again."}
    except Exception as e:
        print("[SUMMARY ERROR]", e)
        return {"error": str(e)}

def get_recent_dialogue(n=3, offset=0):
    try:
        journal = view_journal()
        if not isinstance(journal, list):
            return ""
        start = -(n + offset)
        end = -offset if offset > 0 else None
        selected = journal[start:end]
        return "\n".join(
            f"User: {entry['user']}\nNova: {entry['nova']}"
            for entry in selected
        )
    except Exception as e:
        print("[RECENT DIALOGUE ERROR]", e)
        return ""

def get_dialogue_by_date(date_str):
    try:
        journal = view_journal()
        filtered = []
        for entry in journal:
            timestamp = entry.get("timestamp", "")
            if timestamp.startswith(date_str):
                filtered.append(f"User: {entry['user']}\nNova: {entry['nova']}")
        return "\n".join(filtered) if filtered else "No entries found for that date."
    except Exception as e:
        print("[DIALOGUE DATE ERROR]", e)
        return "Something went wrong while searching by date."

def search_journal_by_keyword(keyword):
    try:
        journal = view_journal()
        keyword = keyword.lower()
        matches = [
            f"{entry['timestamp']}\nUser: {entry['user']}\nNova: {entry['nova']}"
            for entry in journal
            if keyword in entry.get("user", "").lower() or keyword in entry.get("nova", "").lower()
        ]
        return "\n\n".join(matches) if matches else "No journal entries matched that keyword."
    except Exception as e:
        print("[JOURNAL SEARCH ERROR]", e)
        return "Something went wrong during keyword search."

def extract_journal_tags():
    try:
        journal = view_journal()
        tag_set = set()
        for entry in journal:
            combined_text = f"{entry.get('user', '')} {entry.get('nova', '')}".lower()
            for word in combined_text.split():
                word = word.strip(".,!?()[]\"'")
                if len(word) > 4 and word.isalpha():
                    tag_set.add(word)
        return sorted(tag_set)
    except Exception as e:
        print("[TAG EXTRACTION ERROR]", e)
        return []

def route_to_memory(entry):
    try:
        content = f"{entry.get('user', '')} {entry.get('nova', '')}".lower()
        if "xtts" in content or "voice" in content:
            save_to_memory("memory/model_debug.json", entry)
        elif "goal" in content or "plan" in content:
            save_to_memory("memory/user_goals.json", entry)
        elif "error" in content or "fix" in content:
            save_to_memory("memory/model_debug.json", entry)
        elif "layout" in content or "portfolio" in content:
            save_to_memory("memory/feature_feedback.json", entry)
        elif "feedback" in content or "reaction" in content:
            save_to_memory("memory/feature_feedback.json", entry)
        else:
            # Fallback: dump into session summary for uncategorized entries
            save_to_memory("memory/session_summary.json", entry)
    except Exception as e:
        print("[ROUTE MEMORY ERROR]", e)