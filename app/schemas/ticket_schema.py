from pydantic import BaseModel
from typing import Optional
from datetime import datetime



# --------- Request Schema (Incoming Ticket) ---------

class TicketCreate(BaseModel):
    customer_id: str
    order_id: Optional[str] = None
    issue_text: str

# --------- Resolved Schema ---------

class TicketResolve(BaseModel):
    resolved: bool = True
    

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

    # SLA Tracking
    resolved_at: Optional[datetime]
    resolution_time_hours: Optional[float]
    sla_breached: Optional[bool]

    # Ticket Lifecycle
    status: str

    class Config:
        from_attributes = True


class TicketOverride(BaseModel):
    new_priority: str
    override_reason: str
