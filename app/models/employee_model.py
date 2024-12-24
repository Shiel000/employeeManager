from sqlalchemy import Column, Integer, String, Date , Table,ForeignKey
from sqlalchemy.orm import validates, relationship
from app.models.base import Base

class EmployeeModel(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    legajo = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    documento = Column(String, unique=True, nullable=False)
    fecha_ingreso = Column(Date, nullable=False)
    
    
    employee_position_association = Table(
    "employee_position",
    Base.metadata,
    Column("employee_id", Integer, ForeignKey("employees.id"), primary_key=True),
    Column("position_id", Integer, ForeignKey("positions.id"), primary_key=True),
    keep_existing=True)
    
    positions = relationship(
        "PositionModel",
        secondary=employee_position_association,
        back_populates="employees"
    )
    
    