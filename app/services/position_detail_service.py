from sqlalchemy.orm import Session
from app.repositories.position_repository import PositionRepository
from app.repositories.position_detail_repository import PositionDetailRepository
from app.dtos.position_detail_dto import PositionDetailCreateDTO
from app.models.position_detail_model import PositionDetailModel
from app.models.position_model import PositionModel
from datetime import date


class PositionDetailService:
    def __init__(self, db: Session):
        self.detail_repository = PositionDetailRepository(db)
        self.db = db

    
    def create_detail(self, position: PositionModel, detail_data: PositionDetailCreateDTO):
        if not position.active:
            raise ValueError("Cannot add details to an inactive position")

        latest_detail = self.detail_repository.get_latest_by_position(position.id)
        if latest_detail:
            if detail_data.start_date <= latest_detail.end_date:
                raise ValueError("New detail start_date must be after the active detail's end_date")
            latest_detail.end_date = detail_data.start_date
            self.detail_repository.update(latest_detail)

        new_detail = PositionDetailModel(
            salary=detail_data.salary,
            start_date=detail_data.start_date,
            end_date=detail_data.end_date,
            position=position
        )
        self.detail_repository.create(new_detail)
        return new_detail
    
    def update_active_detail(self, position: PositionModel, new_salary: float):
        
        latest_detail = self.detail_repository.get_latest_by_position(position.id)
        if not latest_detail:
            raise ValueError("No active detail found for this position")

        latest_detail.end_date = date.today()
        self.detail_repository.update(latest_detail)
        new_detail = PositionDetailModel(
            salary=new_salary,
            start_date=date.today(),
            end_date=None,
            position=position
        )
        self.detail_repository.create(new_detail)
        return new_detail
    
    def get_active_detail(self, position_id: int):
        return self.detail_repository.get_latest_by_position(position_id)
    