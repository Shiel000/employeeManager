from sqlalchemy.ext.asyncio import AsyncSession
from app.services.position_service import PositionService
from app.dtos.position_dto import PositionCreateDTO,PositionUpdateDTO,PositionOutDTOWithDetailDTO,PositionFilterDTO
from app.models.position_model import PositionModel
from fastapi_pagination import Page,Params
from typing import Optional

class PositionController:
    def __init__(self, db: AsyncSession,params = None):
        self.service = PositionService(db)
        self.params =params

    async def create_position(self, position_data: PositionCreateDTO) -> PositionModel:
        return await self.service.create_position(position_data)
    
    async def get_all_positions(self,  filters: Optional[PositionFilterDTO]) -> Page[PositionOutDTOWithDetailDTO]:
        return await self.service.get_all_positions(filters=filters)
    
    async def get_position(self, position_id: int) -> Optional[dict]:
        return await self.service.get_position(position_id)
    
    async def edit_position(self, position_id: int, position_data: PositionUpdateDTO):
        return await self.service.edit_position(position_id, position_data)

    async def deactivate_position(self, position_id: int):
        return await self.service.update_active_status(position_id, is_active=False)
    
    async def activate_position(self, position_id: int):
        return await self.service.update_active_status(position_id, is_active=True)
            
    async def delete_position(self, position_id: int):
        await self.service.delete_position(position_id)
    