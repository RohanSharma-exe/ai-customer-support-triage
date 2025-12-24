from app.ai.intent_classifier import predict_intent
from app.ai.sentiment_analyzer import analyze_sentiment
from app.ai.urgency_detector import detect_urgency

def analyze_ticket_text(text: str) -> dict:
    intent, intent_conf = predict_intent(text)
    sentiment, sentiment_conf = analyze_sentiment(text)
    urgency, urgency_conf = detect_urgency(text)

    return {
        "intent": intent,
        "sentiment": sentiment,
        "urgency": urgency,
        "confidence": min(intent_conf, sentiment_conf, urgency_conf)
    }
