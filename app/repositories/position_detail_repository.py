from sqlalchemy.orm import Session
from app.models.position_detail_model import PositionDetailModel

class PositionDetailRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, detail_id: int):
        return self.db.query(PositionDetailModel).filter(PositionDetailModel.id == detail_id).first()

    def get_latest_by_position(self, position_id: int):
        return (
            self.db.query(PositionDetailModel)
            .filter(PositionDetailModel.position_id == position_id, PositionDetailModel.end_date == None)
            .first()
        )

    def create(self, detail: PositionDetailModel):
        self.db.add(detail)
        return detail

    def update(self, detail: PositionDetailModel):
        self.db.commit()
        return detail
    
    # def delete_by_position_id(self, position_id: int):

    #     self.db.query(PositionDetailModel).filter(PositionDetailModel.position_id == position_id).delete()
    
    def delete_by_position_id(self, position_id: int):
        deleted_count = (
            self.db.query(PositionDetailModel)
            .filter(PositionDetailModel.position_id == position_id)
            .delete(synchronize_session=False)
        )



    