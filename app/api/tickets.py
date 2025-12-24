from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.ticket_schema import TicketCreate, TicketResponse, TicketResolve
from app.services.ticket_service import create_ticket, resolve_ticket
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TicketResponse)
def create_support_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db)
):
    return create_ticket(db, ticket)


@router.post("/{ticket_id}/resolve", response_model=TicketResponse)
def resolve_support_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    ticket = resolve_ticket(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket

