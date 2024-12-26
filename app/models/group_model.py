from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class GroupModel(Base):
    __tablename__ = "group"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(250), nullable=False)
