# Keyword-based crisis detection.
# This is intentionally broad and imperfect — it's a safety net, not a diagnosis tool.
# When in doubt, it should trigger and show resources rather than stay silent.

CRISIS_KEYWORDS = [
    "suicide", "suicidal", "kill myself", "end my life", "want to die",
    "don't want to live", "no reason to live", "better off dead",
    "self harm", "self-harm", "hurt myself", "cutting myself",
    "can't go on", "can't take it anymore", "ending it all",
]

INDIA_CRISIS_RESOURCES = (
    "I want to make sure you get real support right now, not just a chat reply.\n\n"
    "Please reach out to one of these — they're free and confidential:\n\n"
    "• iCall: 9152987821 (Mon–Sat, 10am–8pm)\n"
    "• Vandrevala Foundation: 1860-2662-345 (24/7)\n"
    "• KIRAN Mental Health Helpline: 1800-599-0019 (24/7)\n\n"
    "If you're in immediate danger, please call 112 or go to your nearest hospital.\n\n"
    "You don't have to go through this alone — is there someone close to you, "
    "like a friend or family member, you could also reach out to right now?"
)


def contains_crisis_language(text: str) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in CRISIS_KEYWORDS)