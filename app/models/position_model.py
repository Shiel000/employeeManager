from sqlalchemy import Column, Integer, String, Date , Table,ForeignKey,Float
from sqlalchemy.orm import relationship
from app.models.base import Base

class PositionModel(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)  # Puede ser nulo si el cargo está activo
    importe = Column(Float, nullable=False)

    # Many-to-many relationship with employees
    employee_position_association = Table(
        "employee_position",
        Base.metadata,
        Column("employee_id", Integer, ForeignKey("employees.id"), primary_key=True),
        Column("position_id", Integer, ForeignKey("positions.id"), primary_key=True),
        keep_existing=True)   
        
    employees = relationship(
            "PositionModel",
            secondary=employee_position_association,
            back_populates="employees"
        )