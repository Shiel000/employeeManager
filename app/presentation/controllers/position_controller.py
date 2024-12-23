from sqlalchemy.orm import Session
from app.application.services.position_service import PositionService
from app.application.dtos.position_dto import PositionCreateDTO, PositionUpdateDTO

class PositionController:
    def __init__(self, db: Session):
        self.service = PositionService(db)

    def get_all_positions(self, include_salaries: bool = True):
        positions = self.service.get_all_positions()
        # Lógica específica de presentación: filtrar datos
        if not include_salaries:
            for position in positions:
                del position.importe  # Elimina el campo 'importe' de la respuesta
        return positions

    def get_position(self, position_id: int):
        try:
            return self.service.get_position(position_id)
        except ValueError:
            raise ValueError("Position not found")  # Transformar error genérico

    def create_position(self, position_data: PositionCreateDTO):
        # Validación específica del cliente (ejemplo)
        if position_data.importe < 0:
            raise ValueError("Salary cannot be negative")
        return self.service.create_position(position_data)

    def update_position(self, position_id: int, position_data: PositionUpdateDTO):
        # Transformación: ignorar actualizaciones de ciertos campos (ejemplo)
        if "descripcion" in position_data.dict(exclude_unset=True):
            raise ValueError("Description cannot be updated")
        return self.service.update_position(position_id, position_data)

    def delete_position(self, position_id: int):
        try:
            self.service.delete_position(position_id)
        except ValueError:
            raise ValueError("Position not found or cannot be deleted")
