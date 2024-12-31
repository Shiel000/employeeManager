from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base 

class EmployeePosition(Base):
    __tablename__ = "employee_position"
    employee_id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    position_id = Column(Integer, ForeignKey("position.id"), primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True) 

    employee = relationship("EmployeeModel", back_populates="employee_positions",lazy="selectin")
    position = relationship("PositionModel", back_populates="employee_positions",lazy="selectin")
