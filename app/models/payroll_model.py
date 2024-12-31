from sqlalchemy import Column, Integer, String, Date , Table,ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class PayrollModel(Base):
    __tablename__ = "payroll"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    period = Column(String(7), nullable=False)  # Format "YYYY-MM"
    amount = Column(Numeric(10, 2), nullable=False)  # Column(Numeric(scale=2, precision=15, asdecimal=False, decimal_return_scale=None))
    
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)  # FK to employees table
    employee = relationship("EmployeeModel",lazy="selectin")
    
