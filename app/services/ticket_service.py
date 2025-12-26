from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.ticket import Ticket
from app.models.prediction import Prediction
from app.schemas.ticket_schema import TicketCreate
from app.services.decision_service import analyze_ticket_text
from app.services.routing_service import route_ticket
from app.services.reply_assist_service import create_reply_draft

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
        confidence=decision["confidence"],
        explanation=f"Intent={decision['intent']}, Urgency={decision['urgency']}, Sentiment={decision['sentiment']}"
    )

    db.add(prediction)
    db.commit()

    # Routing Engine
    agent, _ = route_ticket(
        db=db,
        intent=decision["intent"],
        priority=decision["priority"],
        sla_risk=decision["sla_risk"]
    )

    if agent:
        ticket.assigned_agent_id = agent.id
        agent.active_tickets += 1

    # AI-Assisted Reply (Draft only)
    reply = create_reply_draft(
        intent=decision["intent"],
        sentiment=decision["sentiment"],
        urgency=decision["urgency"],
        order_id=ticket.order_id
    )

    # Store draft on ticket (simple approach)
    # Optional: add a new column later (reply_draft TEXT)
    ticket.status = "OPEN"  # unchanged; draft is for agent view

    db.commit()
    db.refresh(ticket)

    # Return ticket; draft can be returned via a read endpoint later
    return ticket

def resolve_ticket(db: Session, ticket_id: int) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        return None

    ticket.status = "RESOLVED"
    ticket.resolved_at = datetime.now(timezone.utc)

    # 🔑 Normalize created_at to UTC-aware
    ticket.created_at = ticket.created_at.replace(tzinfo=timezone.utc)

    # Compute resolution time
    resolution_delta = ticket.resolved_at - ticket.created_at
    ticket.resolution_time_hours = resolution_delta.total_seconds() / 3600

    # SLA check
    if ticket.sla_hours and ticket.resolution_time_hours > ticket.sla_hours:
        ticket.sla_breached = True
    else:
        ticket.sla_breached = False

    db.commit()
    db.refresh(ticket)

    return ticket

def override_ticket_priority(
    db: Session,
    ticket_id: int,
    new_priority: str,
    reason: str
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    prediction = (
        db.query(Prediction)
        .filter(Prediction.ticket_id == ticket_id)
        .order_by(Prediction.id.desc())
        .first()
    )

    if not ticket or not prediction:
        return None

    ticket.priority = new_priority

    prediction.is_overridden = True
    prediction.override_reason = reason

    db.commit()
    db.refresh(ticket)

    return ticket
