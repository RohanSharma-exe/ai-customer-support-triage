from app.ai.intent_classifier import predict_intent
from app.ai.sentiment_analyzer import analyze_sentiment
from app.ai.urgency_detector import detect_urgency
from app.ai.sla_predictor import predict_sla_risk

def analyze_ticket_text(text: str) -> dict:
    intent, _ = predict_intent(text)
    sentiment, _ = analyze_sentiment(text)
    urgency, _ = detect_urgency(text)

    # Priority Assignment
    if intent == "PAYMENT_ISSUE" or (urgency == "HIGH" and sentiment == "NEGATIVE"):
        priority = "P1"
    elif intent in ["ORDER_DELAY", "REFUND_RETURN"]:
        priority = "P2"
    else:
        priority = "P3"

    sla_risk = predict_sla_risk(intent, urgency, priority)

    return {
        "intent": intent,
        "sentiment": sentiment,
        "urgency": urgency,
        "priority": priority,
        "sla_risk": sla_risk
    }
