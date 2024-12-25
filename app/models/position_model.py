from sqlalchemy import Column, Integer, String, Date , Table,ForeignKey,Float
from sqlalchemy.orm import relationship
from app.models.base import Base

class PositionModel(Base):
    __tablename__ = "position"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # Puede ser nulo si el cargo está activo
    general_id = Column(Integer, ForeignKey("general.id"), nullable=True)
    general = relationship("GeneralModel")

    # Many-to-many relationship with employees
    employee_position_association = Table(
        "employee_position",
        Base.metadata,
        Column("employee_id", Integer, ForeignKey("employee.id"), primary_key=True),
        Column("position_id", Integer, ForeignKey("position.id"), primary_key=True),
        keep_existing=True)   
    
    employees = relationship("EmployeeModel",secondary=employee_position_association,back_populates="positions")
