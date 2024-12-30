from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base  # Asegúrate de que apunte correctamente a tu Base declarativa

class EmployeePosition(Base):
    __tablename__ = "employee_position"
    employee_id = Column(Integer, ForeignKey("employee.id"), primary_key=True)
    position_id = Column(Integer, ForeignKey("position.id"), primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)  # NULL si el cargo está activo

    # Relación inversa opcional
    employee = relationship("EmployeeModel", back_populates="employee_positions",lazy="selectin")
    position = relationship("PositionModel", back_populates="employee_positions",lazy="selectin")
