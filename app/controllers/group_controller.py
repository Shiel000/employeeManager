from sqlalchemy.orm import Session
from app.services.group_service import GroupService
from app.dtos.group_dto import GroupCreateDTO, GroupUpdateDTO

class GroupController:
    def __init__(self, db: Session):
        self.service = GroupService(db)

    def get_all_groups(self, include_positions: bool = True):
        groups = self.service.get_all_groups()
        # Lógica específica de presentación: filtrar datos relacionados (por ejemplo, posiciones)
        if not include_positions:
            for group in groups:
                group.positions = []  # Excluir las posiciones de la respuesta
        return groups

    def get_group(self, group_id: int):
        group = self.service.get_group(group_id)
        if not group:
            raise ValueError("group not found")
        return group

    def create_group(self, group_data: GroupCreateDTO):
        return self.service.create_group(group_data)

    
    def update_group(self, group_id: int, group_data: GroupUpdateDTO):
        # Lógica delegada completamente al servicio
        return self.service.update_group(group_id, group_data)

    def delete_group(self, group_id: int):
        # Simplemente delega la lógica al servicio
        return self.service.delete_group(group_id)

