from sqlalchemy.orm import Session
from app.models.position_model import PositionModel
from app.models.position_detail_model import PositionDetailModel
from app.models.employee_position_table import EmployeePosition
from typing import  List
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional



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
        
    async def get_all(self) -> List[PositionModel]:
        query = select(PositionModel)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def __init__(self, db: Session):
    #     self.db = db

    # def get_all(self):
    #     return self.db.query(PositionModel).all()

    # def get_by_id(self, position_id: int):
    #     return self.db.query(PositionModel).filter(PositionModel.id == position_id).first()

    # def create(self, position: PositionModel):
    #     # Makes and add but not commit
    #     self.db.add(position)
    #     return position

    # def delete(self, position: PositionModel):
    #     self.db.delete(position)

    # def has_details(self, position_id: int) -> bool:
    #     return (
    #         self.db.query(PositionDetailModel)
    #         .filter(PositionDetailModel.position_id == position_id)
    #         .count() > 0
    #     )
   
    # def get_by_name(self, name: str):
    #     return self.db.query(PositionModel).filter(PositionModel.description == name).first()
    
    # def get_by_ids(self, position_ids: List[int], is_active: bool = False):
    #     query = self.db.query(PositionModel).filter(PositionModel.id.in_(position_ids))
    #     if is_active:
    #         query = query.filter(PositionModel.active == True)
    #     return query.all()
    
    # def delete(self, position: PositionModel):
    #     self.db.delete(position)

    # def get_related_employees(self, position_id: int):
    #     return (self.db.query(EmployeePosition).filter(EmployeePosition.position_id == position_id).all())

    