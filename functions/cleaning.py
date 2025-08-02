import json
import os

# Load planning markers from JSON file
def load_markers():
    path = os.path.join("filters", "planning_markers.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Clean Qwen output by removing lines with planning markers
def clean_qwen_output(text):
    markers = load_markers()
    lines = text.split("\n")
    return "\n".join([
        line for line in lines
        if not any(marker.lower() in line.lower() for marker in markers)
    ])

# Optional: Log raw output for debugging and filter updates
def log_raw_output(text):
    os.makedirs("logs", exist_ok=True)
    path = os.path.join("logs", "raw_qwen_output.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(text + "\n\n")