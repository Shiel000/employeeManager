# from sqlalchemy.orm import Session
from app.services.employee_service import EmployeeService
from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO,EmployeeAddDeletePositionsDTO,EmployeeFilter
from typing import Optional
from fastapi_pagination import Page
from app.models.employee_model import EmployeeModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


class EmployeeController:

    def __init__(self, db: AsyncSession,params=None):
        self.service = EmployeeService(db,params)
        self.params =params
        
    async def get_all_employees(self, filters: Optional[EmployeeFilter], include_positions: bool) -> Page[EmployeeModel]:
        return await self.service.get_all_employees(filters, include_positions)

    async def create_employee(self, employee_data: EmployeeCreateDTO) -> EmployeeModel:
        return await self.service.create_employee(employee_data)

    async def get_employee(self, employee_id: int) -> Optional[dict]:
        return await self.service.get_employee(employee_id)

    async def update_employee(self, employee_id: int, update_data: EmployeeUpdateDTO) -> EmployeeModel:
        return await self.service.update_employee(employee_id, update_data)

    async def delete_employee(self, employee_id: int) -> dict:
        return await self.service.delete_employee(employee_id)

    async def add_positions(self, employee_id: int, positions: EmployeeAddDeletePositionsDTO) -> EmployeeModel:
        return await self.service.add_positions_to_employee(employee_id, positions.positions)

    async def remove_positions(self, employee_id: int, positions: EmployeeAddDeletePositionsDTO) -> EmployeeModel:
        return await self.service.remove_positions_from_employee(employee_id, positions.positions)

    async def get_position_history(self, employee_id: Optional[int] = None, employee_number: Optional[int] = None) -> List[dict]:
        return await self.service.get_position_history(employee_id=employee_id, employee_number=employee_number)









    # def __init__(self, db: Session,params=None):
    #     self.service = EmployeeService(db,params)
    #     self.params =params  
    # def create_employee(self, employee_data: EmployeeCreateDTO):
    #     return self.service.create_employee(employee_data)
    
    # def update_employee(self, employee_id: int, update_data: EmployeeUpdateDTO):
    #     return self.service.update_employee(employee_id, update_data)
    
    # def add_positions(self, employee_id: int, positions: EmployeeAddDeletePositionsDTO):
    #     return self.service.add_positions_to_employee(employee_id, positions.positions)
    
    # def remove_positions(self, employee_id: int, positions: EmployeeAddDeletePositionsDTO):
    #     return self.service.remove_positions_from_employee(employee_id, positions.positions)
    
    # def get_position_history(self, employee_id: Optional[int] = None, employee_number: Optional[int] = None):
    #     return self.service.get_position_history(employee_id=employee_id, employee_number=employee_number)
    
    # def get_employee(self, employee_id: int):
    #     return self.service.get_employee(employee_id)
    
    # def delete_employee(self, employee_id: int):
    #     return self.service.delete_employee(employee_id)
    
    # def get_all_employees(self, filters: Optional[EmployeeFilter], include_positions: bool):
    #     # Pasa el flag `include_positions` al servicio
    #     return self.service.get_all_employees(filters, include_positions)