from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.routes import employee_routes, position_routes, payroll_routes,health_routes, version_routes,populate_routes
from app.models.base import Base, engine
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
import os
from app.utils.seed import populate_dummy_data


# engine = create_async_engine(os.getenv("DATABASE_URL"), echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()

# Register routes
app.include_router(employee_routes.router, prefix="/api/employees", tags=["Employees"])
app.include_router(position_routes.router, prefix="/api/positions", tags=["Positions"])
app.include_router(payroll_routes.router, prefix="/api/payrolls", tags=["Payrolls"])
app.include_router(populate_routes.router, prefix="/api/populate", tags=["Populate"])
app.include_router(health_routes.router, tags=["Health"])
app.include_router(version_routes.router, tags=["Version"])


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
