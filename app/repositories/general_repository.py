from sqlalchemy.orm import Session
from app.models.general_model import GeneralModel

class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(GeneralModel).all()

    def get_by_id(self, general_id: int):
        return self.db.query(GeneralModel).filter(GeneralModel.id == general_id).first()
    
    def get_generals_by_group_id(self,group_id:int):
        return self.db.query(GeneralModel).filter(GeneralModel.group_id == group_id).all()

    def create(self, general: GeneralModel):
        self.db.add(general)
        self.db.commit()
        self.db.refresh(general)
        return general

    def update(self, general: GeneralModel):
        self.db.commit()
        return general

    def delete(self, general: GeneralModel):
        self.db.delete(general)
        self.db.commit()
