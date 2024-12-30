from sqlalchemy.orm import Session
from app.models.employee_position_table import EmployeePosition
from typing import  List
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def __init__(self, db: Session):
    #     self.db = db
        
        
    # def get_related_employees(self, position_id: int):
    #     return (
    #         self.db.query(EmployeePosition)
    #         .filter(EmployeePosition.position_id == position_id)
    #         .all()
    #     )

    # def get_active_relationships(self, employee_id: int, position_ids: List[int]):
    #     """
    #     Obtiene las relaciones activas entre un empleado y una lista de posiciones.
    #     """
    #     return (
    #         self.db.query(EmployeePosition)
    #         .filter(
    #             EmployeePosition.employee_id == employee_id,
    #             EmployeePosition.position_id.in_(position_ids),
    #             EmployeePosition.end_date == None
    #         )
    #         .all()
    #     )

    # def update_relationship_end_date(self, relationships: List[EmployeePosition], end_date: date):
    #     for relationship in relationships:
    #         relationship.end_date = end_date
            
    # def create(self, employee: EmployeePosition):
    #     self.db.add(employee)
    #     return employee

    # def get_active_positions_by_employee(self, employee_id: int):
    #     return (self.db.query(EmployeePosition).filter(
    #             EmployeePosition.employee_id == employee_id,
    #             EmployeePosition.end_date == None
    #         )
    #         .all())
    
