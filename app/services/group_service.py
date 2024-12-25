from sqlalchemy.orm import Session
from app.repositories.group_repository import GroupRepository
from app.dtos.group_dto import GroupCreateDTO, GroupUpdateDTO
from app.models.group_model import GroupModel

class GroupService:
    def __init__(self, db: Session):
        self.repository = GroupRepository(db)

    def get_all_groups(self):
        return self.repository.get_all()

    def get_group(self, group_id: int):
        return self.repository.get_by_id(group_id)

    def create_group(self, group_data: GroupCreateDTO):
        group = GroupModel(**group_data.dict())
        return self.repository.create(group)

    def update_group(self, group_id: int, group_data: GroupUpdateDTO):
        group = self.repository.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")

        for key, value in group_data.dict(exclude_unset=True).items():
            setattr(group, key, value)

        return self.repository.update(group)


    def delete_group(self, group_id: int):
        group = self.repository.get_by_id(group_id)
        if not group:
            raise ValueError("group not found")
        self.repository.delete(group)