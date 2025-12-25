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

def model_performance(db: Session, risk_threshold: float = 0.7) -> dict:
    """
    Evaluate SLA risk predictions against actual SLA outcomes.
    """

    predictions = (
        db.query(Prediction, Ticket)
        .join(Ticket, Ticket.id == Prediction.ticket_id)
        .filter(Ticket.status == "RESOLVED")
        .all()
    )

    tp = fp = fn = tn = 0

    for pred, ticket in predictions:
        predicted_high_risk = pred.sla_risk_score >= risk_threshold
        actual_breach = ticket.sla_breached

        if predicted_high_risk and actual_breach:
            tp += 1
        elif predicted_high_risk and not actual_breach:
            fp += 1
        elif not predicted_high_risk and actual_breach:
            fn += 1
        else:
            tn += 1

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0

    return {
        "risk_threshold": risk_threshold,
        "total_evaluated_tickets": len(predictions),
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
    }
