from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.routes import employee_routes
from app.models.base import Base, engine
from app.routes import position_routes

app = FastAPI()

# Register routes
app.include_router(employee_routes.router, prefix="/api/employees", tags=["Employees"])
app.include_router(position_routes.router, prefix="/api/positions", tags=["Positions"])

# Create tables
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
