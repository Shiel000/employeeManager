from app.dtos.position_dto import PositionCreateDTO, PositionUpdateDTO, PositionOutDTO,PositionOutDTOWithDetailDTO,PositionFilterDTO
from app.repositories.employee_position_repository import EmployeePositionRepository
from app.repositories.position_detail_repository import PositionDetailRepository
from app.services.position_detail_service import PositionDetailService
from app.repositories.position_repository import PositionRepository
from app.models.position_model import PositionModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page,paginate
from typing import Optional



class PositionService:
    def __init__(self, db: AsyncSession,params=None):
        self.position_repository = PositionRepository(db)
        self.detail_service = PositionDetailService(db)
        self.employee_position_repository = EmployeePositionRepository(db)
        self.detail_repository = PositionDetailRepository(db)
        self.db = db
        self.params =params


    async def create_position(self, position_data: PositionCreateDTO) -> PositionOutDTO:
        existing_position = await self.position_repository.get_by_name(position_data.description)
        if existing_position:
            raise ValueError(f"A position with the name '{position_data.description}' already exists.")
        position = PositionModel(description=position_data.description, active=True)
        await self.position_repository.create(position)
        await self.detail_service.create_detail(position=position, detail_data=position_data.detail)
        await self.db.commit()
        await self.db.refresh(position)

        return PositionOutDTO.from_orm(position)
    
    
    async def get_all_positions(self, filters: PositionFilterDTO) -> Page[PositionOutDTOWithDetailDTO]:
        positions = await self.position_repository.get_all(filters)

        positions_with_details = []
        for position in positions:
            active_detail = await self.detail_service.get_active_detail(position.id)
            positions_with_details.append(PositionOutDTOWithDetailDTO(
                id=position.id,
                description=position.description,
                active=position.active,
                start_date=active_detail.start_date if active_detail else None,
                end_date=active_detail.end_date if active_detail else None,
                salary=active_detail.salary if active_detail else None,
            ))

        return paginate(positions_with_details, self.params)

    async def get_position(self, position_id: int) -> Optional[dict]:
        position = await self.position_repository.get_by_id(position_id)
        if not position:
            raise ValueError("Position not found")
        detail = await self.detail_service.get_active_detail(position_id)
        return {
            "description": position.description,
            "active": position.active,
            "start_date": detail.start_date if detail else None,
            "end_date": detail.end_date if detail else None,
            "salary": detail.salary if detail else None,
        }
        
        
    async def edit_position(self, position_id: int, position_data: PositionUpdateDTO)-> PositionOutDTO:
        position = await self.position_repository.get_by_id(position_id)
        if not position or not position.active:
            raise ValueError("Position not found or inactive")
        new_detail = await self.detail_service.update_active_detail(
            position=position, new_salary=position_data.salary
        )

        await self.db.commit()
        await self.db.refresh(position)
        await self.db.refresh(new_detail) 
        response = PositionOutDTO.from_orm(position)
        response.salary = new_detail.salary
        return response

    async def update_active_status(self, position_id: int, is_active: bool) -> PositionModel:
        position = await self.position_repository.get_by_id(position_id)
        if not position:
            raise ValueError("Position not found")
        position.active = is_active
        await self.db.commit()
        await self.db.refresh(position)
        return position

    async def delete_position(self, position_id: int) -> None:
        position = await self.position_repository.get_by_id(position_id)
        if not position:
            raise ValueError("Position not found.")
        if position.active:
            raise ValueError("Cannot delete an active position.")
        related_employees = await self.employee_position_repository.get_related_employees(position_id)
        if related_employees:
            raise ValueError("Cannot delete position because it is linked to employees.")
        await self.detail_repository.delete_by_position_id(position_id)
        await self.position_repository.delete(position)
        await self.db.commit()

