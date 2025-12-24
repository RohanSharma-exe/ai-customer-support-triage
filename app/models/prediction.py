from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.session import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))

    model_version = Column(String)

    predicted_priority = Column(String)
    sla_risk_score = Column(Float)
    confidence = Column(Float)

    explanation = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
