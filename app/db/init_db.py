from app.db.session import Base, engine
from app.models.ticket import Ticket
from app.models.agent import Agent
from app.models.prediction import Prediction

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized with all tables.")