import json
import os

def load_memory(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[MEMORY LOAD ERROR] {filename}", e)
        return []

def save_to_memory(filename, entry):
    try:
        memory = load_memory(filename)
        memory.append(entry)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)
    except Exception as e:
        print(f"[MEMORY SAVE ERROR] {filename}", e)

def update_memory(filename, entry_id, new_data):
    try:
        memory = load_memory(filename)
        for i, entry in enumerate(memory):
            if entry.get("id") == entry_id:
                memory[i].update(new_data)
                break
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)
    except Exception as e:
        print(f"[MEMORY UPDATE ERROR] {filename}", e)

def clear_memory_by_tag(filename, tag):
    try:
        memory = load_memory(filename)
        new_memory = [entry for entry in memory if tag.lower() not in entry.get("summary", "").lower()]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(new_memory, f, indent=2)
    except Exception as e:
        print(f"[MEMORY CLEAR ERROR] {filename}", e)

# Optional: Legacy support for routes using save_memory()
def save_memory(memory):
    try:
        with open("memory.json", "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)
    except Exception as e:
        print("[LEGACY SAVE ERROR]", e)