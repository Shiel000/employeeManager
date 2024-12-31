from sqlalchemy import Column, Integer, String,ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.models.base import Base

class PayrollModel(Base):
    __tablename__ = "payroll"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(String(7), nullable=False) 
    amount = Column(Numeric(10, 2), nullable=False)
    
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    employee = relationship("EmployeeModel",lazy="selectin")
    
