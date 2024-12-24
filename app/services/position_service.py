from sqlalchemy.orm import Session
from app.repositories.position_repository import PositionRepository
from app.models.position_model import PositionModel
from app.dtos.position_dto import PositionCreateDTO, PositionUpdateDTO

class PositionService:
    def __init__(self, db: Session):
        self.repository = PositionRepository(db)

    def get_all_positions(self):
        return self.repository.get_all()

    def get_position(self, position_id: int):
        position = self.repository.get_by_id(position_id)
        if not position:
            raise ValueError("Position not found")
        return position

    def create_position(self, position_data: PositionCreateDTO):
        position = PositionModel(**position_data.dict())
        return self.repository.create(position)

    def update_position(self, position_id: int, position_data: PositionUpdateDTO):
        position = self.repository.get_by_id(position_id)
        if not position:
            raise ValueError("Position not found")
        for key, value in position_data.dict(exclude_unset=True).items():
            setattr(position, key, value)
        return self.repository.update(position)

    def delete_position(self, position_id: int):
        position = self.repository.get_by_id(position_id)
        if not position:
            raise ValueError("Position not found")
        self.repository.delete(position)
