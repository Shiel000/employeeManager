from sqlalchemy.ext.asyncio import AsyncSession
from app.services.position_service import PositionService
from app.dtos.position_dto import PositionCreateDTO,PositionUpdateDTO,PositionOutWithDetailDTO,PositionFilterDTO
from app.models.position_model import PositionModel
from fastapi_pagination import Page,Params
from typing import Optional

class PositionController:
    def __init__(self, db: AsyncSession,params = None):
        self.service = PositionService(db)
        self.params =params

    async def create_position(self, position_data: PositionCreateDTO) -> PositionModel:
        return await self.service.create_position(position_data)
    
    async def get_all_positions(self,  filters: Optional[PositionFilterDTO]) -> Page[PositionOutWithDetailDTO]:
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
    
    
# class PositionController:
#     def __init__(self, db: Session):
#         self.service = PositionService(db)


#     def get_all_positions(self, include_details: bool = True):
#         if include_details:
#             return self.service.get_all_positions_with_details()
#         else:
#             return self.service.get_all_positions()
    
    
#     def get_position(self, position_id: int, include_detail: bool = True):

#         position = self.service.get_position(position_id)
#         if not position:
#             raise ValueError("Position not found")

#         if include_detail:
#             detail = self.service.detail_service.get_active_detail(position_id)
#             return {
#                 "description": position.description,
#                 "active": position.active,
#                 "start_date": detail.start_date if detail else None,
#                 "end_date": detail.end_date if detail else None,
#                 "salary": detail.salary if detail else None,
#             }

#         return {
#             "description": position.description,
#             "active": position.active,
#         }

#     def create_position(self, position_data: PositionCreateDTO):
#         return self.service.create_position(position_data)
    
#     def edit_position(self, position_data: PositionUpdateDTO):
#         try:
#             return self.service.edit_position(position_data)
#         except ValueError as e:
#             raise ValueError(str(e))

#     def deactivate_position(self, position_id: int):
#         try:
#             return self.service.update_active_status(position_id, is_active=False)
#         except ValueError as e:
#             raise ValueError(str(e))
        
#     def activate_position(self, position_id: int):    
#         return self.service.update_active_status(position_id, is_active=True)

#     def delete_position(self, position_id: int):
#         self.service.delete_position(position_id)
#         return {"detail": "Position deleted successfully"}