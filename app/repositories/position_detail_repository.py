from app.models.position_detail_model import PositionDetailModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from typing import Optional


class PositionDetailRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_latest_by_position(self, position_id: int) -> Optional[PositionDetailModel]:
        query = (
            select(PositionDetailModel)
            .where(PositionDetailModel.position_id == position_id)
            .order_by(PositionDetailModel.start_date.desc())
        )
        result = await self.db.execute(query)
        latest_detail = result.scalars().first() 
        return latest_detail
    
    async def create(self, detail: PositionDetailModel) -> None:
        self.db.add(detail)

    async def update(self, detail: PositionDetailModel) -> None:
        self.db.add(detail)
        
        
    async def get_active_by_position(self, position_id: int) -> Optional[PositionDetailModel]:
        query = (
            select(PositionDetailModel)
            .where(
                PositionDetailModel.position_id == position_id,
                PositionDetailModel.end_date == None  # Detalle activo
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def delete_by_position_id(self, position_id: int) -> None:
        query = delete(PositionDetailModel).where(PositionDetailModel.position_id == position_id)
        await self.db.execute(query)
