from pydantic import BaseModel
from typing import Optional


# --------- Request Schema (Incoming Ticket) ---------

class TicketCreate(BaseModel):
    customer_id: str
    order_id: Optional[str] = None
    issue_text: str


# --------- Response Schema (What API Returns) ---------

class TicketResponse(BaseModel):
    id: int
    customer_id: str
    order_id: Optional[str]

    issue_text: str

    # AI Understanding Layer
    intent: Optional[str]
    sentiment: Optional[str]
    urgency: Optional[str]

    # Decision Engine
    priority: Optional[str]

    # Routing
    assigned_agent_id: Optional[int]

    # Ticket Lifecycle
    status: str

    class Config:
        from_attributes = True
