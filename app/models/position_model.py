from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class PositionModel(Base):
    __tablename__ = "position"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(250), nullable=False)
    active = Column(Boolean)
    
    employee_positions = relationship("EmployeePosition", back_populates="position", cascade="all, delete-orphan")
    
