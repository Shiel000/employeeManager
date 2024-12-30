from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.routes import employee_routes, position_routes, payroll_routes
from app.models.base import Base, engine
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
import os
from app.seed import populate_dummy_data


# Asynchronous Engine and Session
# engine = create_async_engine(os.getenv("DATABASE_URL"), echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()

# Register routes
app.include_router(employee_routes.router, prefix="/api/employees", tags=["Employees"])
app.include_router(position_routes.router, prefix="/api/positions", tags=["Positions"])
# app.include_router(payroll_routes.router, prefix="/api/payrolls", tags=["Payrolls"])


add_pagination(app)
disable_installed_extensions_check()

# Create tables
@app.on_event("startup")
async def create_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    # await populate_dummy_data(async_session)


@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()
    print("Recursos cerrados correctamente")





















# from fastapi import FastAPI
# from app.routes import employee_routes
# from app.models.base import Base, engine
# from app.routes import position_routes
# from app.routes import group_routes
# from fastapi_pagination  import add_pagination
# from fastapi_pagination.utils import disable_installed_extensions_check
# from app.routes import payroll_routes
# from app.seed import populate_dummy_data

# app = FastAPI()

# # Register routes
# app.include_router(employee_routes.router, prefix="/api/employees", tags=["Employees"])
# app.include_router(position_routes.router, prefix="/api/positions", tags=["Positions"])
# app.include_router(payroll_routes.router, prefix="/api/payrolls", tags=["Payrolls"])
# app.include_router(group_routes.router, prefix="/api/groups", tags=["Groups"])

# add_pagination(app)
# # deactivate the warnings
# disable_installed_extensions_check()


# # Create tables
# @app.on_event("startup")
# def create_tables():
#     # Base.metadata.drop_all(bind=engine)
#     # populate_dummy_data()
#     Base.metadata.create_all(bind=engine)

# @app.on_event("shutdown")
# def shutdown_event():
#     engine.dispose()
#     print("Recursos cerrados correctamente")
























# @app.on_event("startup")
# async def startup_event():
#     try:
#         # Probar conexión a la base de datos
#         with engine.connect() as connection:
#             connection.execute("SELECT 1")
#         print("Conexión a la base de datos exitosa")
#     except Exception as e:
#         print(f"Error conectando a la base de datos: {e}")
