from flask import Blueprint, request, jsonify
from functions.memory_func import load_memory, save_memory, save_to_memory
from functions.history_func import load_history, save_history
from functions.journal_func import save_to_journal, summarize_journal, get_recent_dialogue, get_dialogue_by_date
from functions.model_runner import run_model
from functions.prompts import build_nova_prompt
from brain import nova
import datetime
import re

ask_bp = Blueprint("ask", __name__)

def get_user_role(request):
    creator_ip = "192.168.1.10"
    current_ip = request.remote_addr
    return "creator" if current_ip == creator_ip else "guest"

@ask_bp.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "")
    memory = load_memory("memory/user_goals.json")
    user_memory_facts = [entry.get("summary", "") for entry in memory]
    user_role = get_user_role(request)
    print(f"[ROLE DETECTED]: {user_role}")

    if "what did we talk about on" in user_input.lower():
        date_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", user_input)
        if date_match:
            recall_date = date_match.group(1)
            result = get_dialogue_by_date(recall_date)
            return jsonify({"response": result})

    if "review our lessons" in user_input.lower() or "remind me what we studied" in user_input.lower():
        summary = summarize_journal()
        reply = summary.get("summary", "I couldn't pull up our past lessons just yet.")
        return jsonify({"response": reply})

    recent_dialogue = get_recent_dialogue(3)
    prompt = build_nova_prompt(user_input, user_memory_facts, user_role, previous_dialogue=recent_dialogue)

    try:
        raw_output, stderr = run_model(prompt, nova)
        if stderr: print("[MODEL STDERR]", stderr)

        reply = "\n".join([line for line in raw_output.split("\n") if not line.strip().startswith(">>>")]).strip()
        reply = reply or "I'm here, but something glitched—try asking me again?"

        history = load_history()
        history.append({"user": user_input, "nova": reply})
        save_history(history[-50:])
        save_to_journal({"timestamp": datetime.datetime.now().isoformat(), "user": user_input, "nova": reply})

        if "remember that" in user_input.lower():
            save_to_memory("memory/user_goals.json", {
                "timestamp": datetime.datetime.now().isoformat(),
                "summary": user_input
            })

        return jsonify({"response": reply})

    except Exception as e:
        print("[ASK ROUTE ERROR]", e)
        return jsonify({"response": f"Nova hit a snag: {str(e)}"})