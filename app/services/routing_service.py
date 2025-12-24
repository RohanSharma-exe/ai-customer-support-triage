from sqlalchemy.orm import Session
from app.models.agent import Agent

def route_ticket(db: Session, intent: str, priority: str, sla_risk: float):
    agents = (
        db.query(Agent)
        .filter(Agent.is_available == True)
        .all()
    )

    if not agents:
        return None, "No available agents"

    best_agent = None
    best_score = -1
    reason = ""

    for agent in agents:
        score = 0

        # Skill match
        if agent.specialization == intent:
            score += 5
        else:
            score += 1

        # SLA risk weighting
        if sla_risk > 0.7:
            score += agent.sla_compliance_rate * 2

        # Priority handling
        if priority == "P1":
            score += 5
        elif priority == "P2":
            score += 3

        # Load penalty (except P1)
        if priority != "P1":
            score -= agent.active_tickets * 0.5

        if score > best_score:
            best_score = score
            best_agent = agent
            reason = (
                f"Skill={agent.specialization}, "
                f"ActiveTickets={agent.active_tickets}, "
                f"SLACompliance={agent.sla_compliance_rate}"
            )

    return best_agent, reason
