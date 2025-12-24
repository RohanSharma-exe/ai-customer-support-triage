from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.ticket import Ticket
from app.models.prediction import Prediction
from app.models.agent import Agent

def sla_metrics(db: Session) -> dict:
    total = db.query(Ticket).count()
    breached = db.query(Ticket).filter(Ticket.sla_breached == True).count()

    return {
        "total_tickets": total,
        "sla_breached": breached,
        "sla_breach_rate": (breached / total) if total else 0.0
    }

def priority_distribution(db: Session) -> dict:
    rows = (
        db.query(Ticket.priority, func.count(Ticket.id))
        .group_by(Ticket.priority)
        .all()
    )
    return {priority: count for priority, count in rows}

def high_risk_predictions(db: Session, threshold: float = 0.7) -> dict:
    count = (
        db.query(Prediction)
        .filter(Prediction.sla_risk_score >= threshold)
        .count()
    )
    return {
        "threshold": threshold,
        "high_risk_tickets": count
    }

def agent_workload(db: Session) -> list[dict]:
    agents = db.query(Agent).all()
    return [
        {
            "agent_id": a.id,
            "name": a.name,
            "specialization": a.specialization,
            "active_tickets": a.active_tickets,
            "sla_compliance_rate": a.sla_compliance_rate
        }
        for a in agents
    ]
