from typing import Tuple

INTENT_KEYWORDS = {
    "PAYMENT_ISSUE": ["payment", "charged", "deducted", "transaction", "refund failed"],
    "ORDER_DELAY": ["not delivered", "late", "delay", "still waiting"],
    "DAMAGED_PRODUCT": ["damaged", "broken", "defective"],
    "WRONG_ITEM": ["wrong item", "incorrect product"],
    "REFUND_RETURN": ["refund", "return"],
    "ACCOUNT_ISSUE": ["login", "account", "password"]
}

def predict_intent(text: str) -> Tuple[str, float]:
    text_lower = text.lower()

    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return intent, 0.90

    return "UNKNOWN", 0.50
