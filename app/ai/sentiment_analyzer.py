from typing import Tuple

NEGATIVE_WORDS = ["angry", "unacceptable", "bad", "worst", "hate"]
POSITIVE_WORDS = ["thanks", "thank you", "great", "good", "appreciate"]

def analyze_sentiment(text: str) -> Tuple[str, float]:
    text_lower = text.lower()

    for word in NEGATIVE_WORDS:
        if word in text_lower:
            return "NEGATIVE", 0.85

    for word in POSITIVE_WORDS:
        if word in text_lower:
            return "POSITIVE", 0.85

    return "NEUTRAL", 0.70
