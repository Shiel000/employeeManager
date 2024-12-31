from sqlalchemy import Column, Integer, String, Date , Table,ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base

class PositionDetailModel(Base):
    __tablename__ = "position_detail"
    id = Column(Integer, primary_key=True, index=True)    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True) 
    salary = Column(Numeric(scale=2, precision=15, asdecimal=False, decimal_return_scale=None))
    position_id = Column(Integer, ForeignKey("position.id"), nullable=True)
    position = relationship("PositionModel",lazy="selectin")
    
