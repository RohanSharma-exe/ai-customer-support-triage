from fastapi import FastAPI
from app.api import tickets
from app.db.init_db import init_db

app = FastAPI(
    title="AI Customer Support Triage System",
    version="1.0.0"
)

init_db()

app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
