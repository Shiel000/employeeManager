from sqlalchemy.orm import Session
from app.models.group_model import GroupModel

class GroupRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(GroupModel).all()

    def get_by_id(self, group_id: int):
        return self.db.query(GroupModel).filter(GroupModel.id == group_id).first()

    def create(self, group: GroupModel):
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def update(self, group: GroupModel):
        self.db.commit()
        return group

    def delete(self, group: GroupModel):
        self.db.delete(group)
        self.db.commit()
