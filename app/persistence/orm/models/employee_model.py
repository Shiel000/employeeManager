from sqlalchemy import Column, Integer, String, Date
from app.persistence.orm.base import Base

class EmployeeModel(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    legajo = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    documento = Column(String, unique=True, nullable=False)
    fecha_ingreso = Column(Date, nullable=False)
