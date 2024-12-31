from sqlalchemy.orm import Session
from app.models.employee_model import EmployeeModel
from app.models.employee_position_table import EmployeePosition
from app.models.position_model import PositionModel
from typing import List
from sqlalchemy.orm import Query
from typing import List, Optional
from app.dtos.employee_dto import EmployeeFilter
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload

from sqlalchemy.ext.asyncio import AsyncSession


class EmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_by_document(self, document: int) -> EmployeeModel:
        query = select(EmployeeModel).where(EmployeeModel.document == document)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def calculate_employee_number(self) -> int:
        last_employee = await self.get_last_employee()
        return last_employee.employee_number + 1 if last_employee else 1

    async def get_last_employee(self) -> EmployeeModel:
        query = select(EmployeeModel).order_by(EmployeeModel.id.desc()).limit(1)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, employee: EmployeeModel):
        self.db.add(employee)
        

    async def get_by_id(self, employee_id: int) -> Optional[EmployeeModel]:
        query = select(EmployeeModel).where(EmployeeModel.id == employee_id)
        result = await self.db.execute(query)  
        return result.scalars().first()
    
    async def update(self, employee: EmployeeModel)-> EmployeeModel:
        self.db.add(employee)  
        await self.db.commit() 
        return employee
        

    async def delete(self, employee: EmployeeModel):
        await self.db.delete(employee)
    
    async def get_by_employee_number(self, employee_number: int)-> Optional[EmployeeModel]:
        query = (
            select(EmployeeModel)
            .options(
                selectinload(EmployeeModel.employee_positions).selectinload(EmployeePosition.position)
            )
            .where(EmployeeModel.employee_number == employee_number)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def filter_by_params(self, filters: Optional[EmployeeFilter]) -> List[EmployeeModel]:
        query = select(EmployeeModel).options(selectinload(EmployeeModel.employee_positions))
        if filters.name:
            query = query.where(EmployeeModel.name.ilike(f"%{filters.name}%"))
        if filters.surname:
            query = query.where(EmployeeModel.surname.ilike(f"%{filters.surname}%"))
        if filters.position is not None:
            query = query.join(EmployeePosition).where(EmployeePosition.position_id == filters.position)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_employee_positions(self, employee_id: int)-> List[EmployeePosition]:
        query = (
            select(EmployeePosition)
            .options(joinedload(EmployeePosition.position))
            .where(EmployeePosition.employee_id == employee_id)
        )
        result = await self.db.execute(query)
        return result.scalars().all() 
    
    
    async def get_all(self) -> List[EmployeeModel]:
        query = select(EmployeeModel)
        result = await self.db.execute(query)
        return result.scalars().all()
