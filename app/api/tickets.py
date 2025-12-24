from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.ticket_schema import TicketCreate, TicketResponse
from app.services.ticket_service import create_ticket
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
