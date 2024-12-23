from sqlalchemy.orm import Session
from app.persistence.orm.models.position_model import PositionModel

class PositionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(PositionModel).all()

    def get_by_id(self, position_id: int):
        return self.db.query(PositionModel).filter(PositionModel.id == position_id).first()

    def create(self, position: PositionModel):
        self.db.add(position)
        self.db.commit()
        self.db.refresh(position)
        return position

    def update(self, position: PositionModel):
        self.db.commit()
        return position

    def delete(self, position: PositionModel):
        self.db.delete(position)
        self.db.commit()
