from app.models.position_detail_model import PositionDetailModel
from app.dtos.position_dto import PositionFilterDTO
from app.models.position_model import PositionModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from typing import  List



class PositionRepository:
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_ids(self, position_ids: List[int], is_active: bool = False) -> List[PositionModel]:
        query = select(PositionModel).where(PositionModel.id.in_(position_ids))
        if is_active:
            query = query.where(PositionModel.active == True)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_name(self, name: str) -> Optional[PositionModel]:
        query = select(PositionModel).where(PositionModel.description == name)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, position: PositionModel) -> None:
        self.db.add(position)
        
    async def get_by_id(self, position_id: int) -> PositionModel:
        query = select(PositionModel).where(PositionModel.id == position_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def delete(self, position: PositionModel) -> None:
        await self.db.delete(position)
 
    async def get_all(self, filters: PositionFilterDTO) -> List[PositionModel]:
        query = select(PositionModel).join(PositionDetailModel)

        if filters.start_date:
            query = query.where(PositionDetailModel.start_date >= filters.start_date)
        if filters.salary_min is not None:
            query = query.where(PositionDetailModel.salary >= filters.salary_min)
        if filters.salary_max is not None:
            query = query.where(PositionDetailModel.salary <= filters.salary_max)
        if filters.active is not None:
            query = query.where(PositionModel.active == filters.active)

        result = await self.db.execute(query)
        return result.scalars().all()
