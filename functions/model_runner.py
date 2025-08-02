import subprocess

def run_model(prompt, model_name="qwen3:1.7b"):
    try:
        result = subprocess.run(
            ["ollama", "run", model_name, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"  # ⬅️ Ensures proper decoding of Unicode output
        )

        # 📤 Log raw response to terminal
        print("\n📤 [Nova Raw Output]:\n" + result.stdout.strip() + "\n")

        return result.stdout.strip(), result.stderr

    except Exception as e:
        return "", str(e)