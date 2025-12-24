def predict_sla_risk(intent: str, urgency: str, priority: str) -> float:
    risk = 0.1

    if priority == "P1":
        risk += 0.5
    elif priority == "P2":
        risk += 0.3

    if urgency == "HIGH":
        risk += 0.2
    elif urgency == "MEDIUM":
        risk += 0.1

    if intent == "PAYMENT_ISSUE":
        risk += 0.2

    return min(risk, 0.99)
