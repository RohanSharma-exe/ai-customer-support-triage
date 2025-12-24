from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.prediction import Prediction
from app.schemas.ticket_schema import TicketCreate
from app.services.decision_service import analyze_ticket_text

def create_ticket(db: Session, ticket_data: TicketCreate) -> Ticket:
    ticket = Ticket(
        customer_id=ticket_data.customer_id,
        order_id=ticket_data.order_id,
        issue_text=ticket_data.issue_text,
        status="OPEN"
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # Decision Engine
    decision = analyze_ticket_text(ticket.issue_text)

    ticket.intent = decision["intent"]
    ticket.sentiment = decision["sentiment"]
    ticket.urgency = decision["urgency"]
    ticket.priority = decision["priority"]

    prediction = Prediction(
        ticket_id=ticket.id,
        model_version="v1-rule-based",
        predicted_priority=decision["priority"],
        sla_risk_score=decision["sla_risk"],
        confidence=0.8,
        explanation=f"Intent={decision['intent']}, Urgency={decision['urgency']}, Sentiment={decision['sentiment']}"
    )

    db.add(prediction)
    db.commit()
    db.refresh(ticket)

    return ticket
