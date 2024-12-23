from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.presentation.routes import employee_routes
from app.persistence.orm.base import Base, engine

app = FastAPI()

# Register routes
app.include_router(employee_routes.router, prefix="/api/employees", tags=["Employees"])

# Create tables
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
