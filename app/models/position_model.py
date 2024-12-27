from sqlalchemy import Column, Integer, String, Table,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.employee_position_table import EmployeePosition

class PositionModel(Base):
    __tablename__ = "position"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(250), nullable=False)
    active = Column(Boolean)
    
    employee_positions = relationship("EmployeePosition", back_populates="position", cascade="all, delete-orphan")
    
    # # Many-to-many relationship with employees
    # employee_position_association = Table(
    #     "employee_position",
    #     Base.metadata,
    #     Column("employee_id", Integer, ForeignKey("employee.id"), primary_key=True),
    #     Column("position_id", Integer, ForeignKey("position.id"), primary_key=True),
    #     keep_existing=True)   
    
    # employees = relationship("EmployeeModel",secondary=employee_position_association,back_populates="positions")
