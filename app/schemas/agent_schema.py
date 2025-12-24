from pydantic import BaseModel

class AgentResponse(BaseModel):
    id: int
    name: str
    specialization: str
    active_tickets: int
    is_available: bool

    class Config:
        from_attributes = True
