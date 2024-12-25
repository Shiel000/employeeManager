from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class GeneralModel(Base):
    __tablename__ = "general"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    aux_string1 = Column(String, nullable=True)
    aux_string2 = Column(String, nullable=True)
    aux_int1 = Column(Integer, nullable=True)
    aux_int2 = Column(Integer, nullable=True)
    aux_date1 = Column(Date, nullable=True)
    aux_date2 = Column(Date, nullable=True)
    group_id = Column(Integer, ForeignKey("group.id"))
    group = relationship("GroupModel")
    depends_on_id = Column(Integer, ForeignKey("general.id"), nullable=True)
    depends_on = relationship("GeneralModel", remote_side=[id])
    
    
    # def __init__(self,data):
    #     self.id =data.get("id",None)
    #     self.description =data.get("description",None)
    #     self.aux_string1 = data.get("aux_string1",None)
    #     self.aux_string2 = data.get("aux_string2",None)
    #     self.aux_int1 = data.get("aux_int1",None)
    #     self.aux_int2 = data.get("aux_int2",None)
    #     self.aux_date1 = data.get("aux_date1",None)
    #     self.aux_date2 = data.get("aux_date2",None)
    #     self.group_id = data.get("group_id",None)
    #     self.depends_on_id = data.get("depends_on_id",None)
