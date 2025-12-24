from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.schemas.ticket_schema import TicketCreate

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

    return ticket
