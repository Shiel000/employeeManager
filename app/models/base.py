from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.setting import settings

# Crear el motor asíncrono
engine = create_async_engine(settings.DATABASE_URL, echo=False)  # Centralizado aquí

# Crear una fábrica de sesiones asíncronas
async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

# Base declarativa para los modelos
Base = declarative_base()

# Dependencia para obtener la sesión
async def get_db():
    async with async_session() as session:
        yield session


# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# # from config.settings import settings
# from app.config.setting import settings

# engine = create_engine(settings.DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()



# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()