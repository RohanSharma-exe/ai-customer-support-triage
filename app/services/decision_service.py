from app.ai.intent_classifier import predict_intent
from app.ai.sentiment_analyzer import analyze_sentiment
from app.ai.urgency_detector import detect_urgency
from app.ai.sla_predictor import predict_sla_risk

CONFIDENCE_THRESHOLD = 0.75

def analyze_ticket_text(text: str) -> dict:
    intent, intent_conf = predict_intent(text)
    sentiment, sentiment_conf = analyze_sentiment(text)
    urgency, urgency_conf = detect_urgency(text)

    confidence = min(intent_conf, sentiment_conf, urgency_conf)

    # Priority Assignment
    if intent == "PAYMENT_ISSUE" or (urgency == "HIGH" and sentiment == "NEGATIVE"):
        priority = "P1"
    elif intent in ["ORDER_DELAY", "REFUND_RETURN"]:
        priority = "P2"
    else:
        priority = "P3"

    # 🔐 Confidence Guardrail
    if confidence < CONFIDENCE_THRESHOLD:
        priority = "P2"  # force safe default

    sla_risk = predict_sla_risk(intent, urgency, priority)

    return {
        "intent": intent,
        "sentiment": sentiment,
        "urgency": urgency,
        "priority": priority,
        "sla_risk": sla_risk,
        "confidence": confidence
    }
