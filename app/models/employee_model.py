from sqlalchemy import Column, Integer, String, Date , Table,ForeignKey
from sqlalchemy.orm import validates, relationship
from app.models.base import Base

class EmployeeModel(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, index=True)
    record = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    document = Column(Integer, unique=True, nullable=False)
    entry_date = Column(Date, nullable=False)
    
    
    employee_position_association = Table(
        "employee_position",
        Base.metadata,
        Column("employee_id", Integer, ForeignKey("employee.id"), primary_key=True),
        Column("position_id", Integer, ForeignKey("position.id"), primary_key=True),
        keep_existing=True)
    
    positions = relationship("PositionModel",secondary=employee_position_association)
    
    
