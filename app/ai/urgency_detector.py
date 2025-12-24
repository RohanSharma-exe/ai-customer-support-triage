from typing import Tuple

HIGH_URGENCY = ["immediately", "asap", "now", "urgent", "right away", "cancel"]
MEDIUM_URGENCY = ["soon", "today", "quick", "fast"]

def detect_urgency(text: str) -> Tuple[str, float]:
    text_lower = text.lower()

    for word in HIGH_URGENCY:
        if word in text_lower:
            return "HIGH", 0.90

    for word in MEDIUM_URGENCY:
        if word in text_lower:
            return "MEDIUM", 0.80

    return "LOW", 0.70
