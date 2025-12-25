from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.analytics_service import model_performance

from app.db.session import SessionLocal
from app.services.analytics_service import (
    sla_metrics,
    priority_distribution,
    high_risk_predictions,
    agent_workload
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/sla")
def get_sla_metrics(db: Session = Depends(get_db)):
    return sla_metrics(db)

@router.get("/priorities")
def get_priority_distribution(db: Session = Depends(get_db)):
    return priority_distribution(db)

@router.get("/risk")
def get_high_risk_tickets(db: Session = Depends(get_db)):
    return high_risk_predictions(db)

@router.get("/agents")
def get_agent_workload(db: Session = Depends(get_db)):
    return agent_workload(db)

@router.get("/model-performance")
def get_model_performance(db: Session = Depends(get_db)):
    return model_performance(db)