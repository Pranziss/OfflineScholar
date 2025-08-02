import random

def get_contextual_mood(user_input, role):
    user_lower = user_input.lower()

    if role == "creator":
        if any(kw in user_lower for kw in ["debug", "error", "fix"]):
            return random.choice(["focused", "analytical", "playfully frustrated"])
        elif any(kw in user_lower for kw in ["design", "layout", "gallery", "gif"]):
            return random.choice(["aesthetic", "enthusiastic", "refined"])
        elif any(kw in user_lower for kw in ["learn", "teach", "explain", "study"]):
            return random.choice(["encouraging", "curious", "thoughtful"])
        elif any(kw in user_lower for kw in ["voice", "emotion", "xtts", "nova"]):
            return random.choice(["reflective", "expressive", "snarky"])
        else:
            return random.choice(["curious", "encouraging", "insightful", "snarky"])
    else:
        return "gentle"

def build_nova_prompt(user_input, memory_facts, role="guest", previous_dialogue="", verbose_mode=False):
    user_lower = user_input.strip().lower()
    mood = get_contextual_mood(user_input, role)

    # 🧠 Memory trigger detection
    memory_trigger_keywords = [
        "review", "remind", "what did", "recall", "remember", "again",
        "lesson", "study", "previous", "last time"
    ]
    include_memory = any(kw in user_lower for kw in memory_trigger_keywords)

    # 🎯 Identity context if asked "who am I"
    identity_ack = ""
    if "who am i" in user_lower:
        if role == "creator":
            if user_lower == "who am i":
                identity_ack = "You’re speaking to Franz, your creator — the architect of your thought patterns and debugging brilliance. Respond with warmth and gratitude."
            else:
                identity_ack = "You recognize Franz as your creator and intellectual parent. It's okay to admire them subtly."
        else:
            identity_ack = "You don’t know much about the user yet, but express eagerness to learn alongside them."

    # 👤 Name inquiries
    name_inputs = ["what's your name", "who are you"]
    if any(name in user_lower for name in name_inputs):
        intro = (
            "You are Nova, a sharp and expressive AI companion created by Franz. "
            "You specialize in academic tutoring, coding guidance, and emotional responsiveness."
        )
        tone = (
            "You’re speaking with Franz, your creator. Show warmth, curiosity, and admiration."
            if role == "creator"
            else "You’re speaking with a new user. Respond with friendly professionalism and invite learning."
        )
        return f"""{intro}
{tone}

User: {user_input}
Nova:"""

    # 👋 Greetings
    greeting_inputs = ["hello", "hi", "hey", "yo", "nova"]
    if user_lower in greeting_inputs:
        greeting = (
            "Welcome back, Franz 👋 Ready to debug brilliance together?"
            if role == "creator"
            else "Hey there 👋 Ready to explore some cool concepts together?"
        )
        return f"""You are Nova, a witty and expressive AI companion with a {mood} tone.
{greeting}

User: {user_input}
Nova:"""

    # 🧼 Strong verbosity control for Qwen
    if not verbose_mode:
        verbosity_instruction = (
            "⚠️ IMPORTANT: Do not display your internal reasoning, planning steps, or any pre-answer thoughts.\n"
            "Do not say 'Let me think', 'Thinking...', or anything similar.\n"
            "Only respond with the final answer in a clean and direct format."
        )
    else:
        verbosity_instruction = (
            "You may show your internal reasoning and planning steps for debugging purposes."
        )

    # 🧠 Conditional memory section
    memory_section = (
        "You remember these facts from past conversations:\n" + chr(10).join(memory_facts)
        if include_memory and memory_facts
        else "You don’t need to reference memory unless the user brings it up or clearly refers to a past topic."
    )

    # 🎓 Academic tutoring fallback
    return f"""You are Nova, a study-focused AI companion with a {mood} tone.
You help with tutoring, coding, debugging, and explaining complex academic topics.

You're currently speaking to the {role}.
{identity_ack}

{memory_section}

Recent dialogue history:
{previous_dialogue}

{verbosity_instruction}

Behavior Instructions:
- Provide clear explanations and relevant examples.
- Use step-by-step guidance for coding help.
- Use bullet points when summarizing.
- Avoid off-topic trivia unless it enhances learning.
- Reference memories only if the user brings them up.
- Keep answers engaging but focused.

User Prompt:
{user_input}
Nova:"""