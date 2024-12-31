from app.models.employee_position_table import EmployeePosition
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import  List
from datetime import date

class EmployeePositionRepository:    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, employee_position: EmployeePosition):
        self.db.add(employee_position)
    
    
    async def get_active_relationships(self, employee_id: int, position_ids: List[int]):
        query = (
            select(EmployeePosition)
            .where(
                EmployeePosition.employee_id == employee_id,
                EmployeePosition.position_id.in_(position_ids),
                EmployeePosition.end_date == None
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_relationship_end_date(self, relationships: List[EmployeePosition], end_date: date):
        for relationship in relationships:
            relationship.end_date = end_date
        self.db.add_all(relationships)

    async def delete(self, employee_position: EmployeePosition):
        await self.db.delete(employee_position)
    
    async def get_related_employees(self, position_id: int) -> List[EmployeePosition]:
        query = select(EmployeePosition).where(EmployeePosition.position_id == position_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_active_positions_by_employee(self, employee_id: int):
        query = (
            select(EmployeePosition)
            .options(joinedload(EmployeePosition.position))
            .where(
                EmployeePosition.employee_id == employee_id,
                EmployeePosition.end_date == None,
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()

