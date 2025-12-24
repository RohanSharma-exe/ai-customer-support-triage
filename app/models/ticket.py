from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    order_id = Column(String, nullable=True)

    issue_text = Column(Text, nullable=False)

    intent = Column(String)
    sentiment = Column(String)
    urgency = Column(String)

    priority = Column(String)  # P1 / P2 / P3

    sla_hours = Column(Integer)
    resolution_time_hours = Column(Float, nullable=True)
    sla_breached = Column(Boolean, default=False)

    assigned_agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)

    status = Column(String, default="OPEN")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolution_time_hours = Column(Float, nullable=True)
    sla_breached = Column(Boolean, default=False)
