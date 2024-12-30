from sqlalchemy import Column, Integer, String, Date , Table,ForeignKey
from sqlalchemy.orm import validates, relationship
from app.models.base import Base
from app.models.employee_position_table import EmployeePosition

class EmployeeModel(Base):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    document = Column(Integer, unique=True, nullable=False)
    entry_date = Column(Date, nullable=False)
    
    employee_positions = relationship("EmployeePosition", back_populates="employee", cascade="all, delete-orphan",lazy="selectin")