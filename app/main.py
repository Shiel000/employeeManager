from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.routes import employee_routes
from app.models.base import Base, engine
from app.routes import position_routes
from app.routes import group_routes

app = FastAPI()

# Register routes
app.include_router(employee_routes.router, prefix="/api/employees", tags=["Employees"])
app.include_router(position_routes.router, prefix="/api/positions", tags=["Positions"])
app.include_router(group_routes.router, prefix="/api/groups", tags=["Groups"])

# Create tables
@app.on_event("startup")
def create_tables():
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

# @app.on_event("startup")
# async def startup_event():
#     try:
#         # Probar conexión a la base de datos
#         with engine.connect() as connection:
#             connection.execute("SELECT 1")
#         print("Conexión a la base de datos exitosa")
#     except Exception as e:
#         print(f"Error conectando a la base de datos: {e}")

@app.on_event("shutdown")
def shutdown_event():
    engine.dispose()
    print("Recursos cerrados correctamente")
