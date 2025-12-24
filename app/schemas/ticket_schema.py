from pydantic import BaseModel
from typing import Optional

class TicketCreate(BaseModel):
    customer_id: str
    order_id: Optional[str] = None
    issue_text: str

class TicketResponse(BaseModel):
    id: int
    customer_id: str
    order_id: Optional[str]
    issue_text: str

    intent: Optional[str]
    sentiment: Optional[str]
    urgency: Optional[str]
    priority: Optional[str]

    status: str

    class Config:
        from_attributes = True
