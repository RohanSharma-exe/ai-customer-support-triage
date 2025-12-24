from sqlalchemy import Column, Integer, String, Float, Boolean
from app.db.session import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    specialization = Column(String)  # PAYMENT, LOGISTICS, RETURNS

    active_tickets = Column(Integer, default=0)
    avg_resolution_time = Column(Float)
    sla_compliance_rate = Column(Float)

    is_available = Column(Boolean, default=True)
