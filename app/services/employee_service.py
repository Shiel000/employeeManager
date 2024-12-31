from app.repositories.employee_position_repository import EmployeePositionRepository
from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO,EmployeeFilter
from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.position_repository import PositionRepository
from app.models.employee_position_table import EmployeePosition
from app.repositories.payroll_repository import PayrollRepository
from app.models.employee_model import EmployeeModel
from app.models.position_model import PositionModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, paginate
from typing import List, Optional,Dict
from datetime import date


class EmployeeService:

    def __init__(self, db: AsyncSession,params=None):
        self.db = db
        self.repository = EmployeeRepository(db)
        self.position_repository = PositionRepository(db)
        self.employee_position_repository = EmployeePositionRepository(db)
        self.payroll_repository = PayrollRepository(db)
        self.params =params


    
    async def get_all_employees(self, filters: Optional[EmployeeFilter], include_positions: bool) -> Page[EmployeeModel]:
        query_result = await self.repository.filter_by_params(filters)

        if include_positions:
            for employee in query_result:
                positions = await self.repository.get_employee_positions(employee.id)
                employee.positions = [
                    {
                        "start_date": pos.start_date,
                        "end_date": pos.end_date,
                        "position": {
                            "id": pos.position.id,
                            "description": pos.position.description,
                            "active": pos.position.active,
                        }
                    }
                    for pos in positions
                ]
        return paginate(query_result, self.params)
    
    async def create_employee(self, employee_data: EmployeeCreateDTO) -> Dict:
        try:
            async with self.db.begin():
                await self._validate_document_uniqueness(employee_data.document)
                new_employee = await self._create_new_employee(employee_data)
                positions = await self._validate_and_get_positions(employee_data.positions)
                await self._assign_positions_to_employee(new_employee, positions)
            await self.db.refresh(new_employee)
            return self._build_employee_response(new_employee, positions)
        except Exception as e:
            print(f"Error while creating employee: {e}")
            raise e

    async def _validate_document_uniqueness(self, document: int):
        existing_employee = await self.repository.get_by_document(document)
        if existing_employee:
            raise ValueError("An employee with this document already exists.")

    async def _create_new_employee(self, employee_data: EmployeeCreateDTO) -> EmployeeModel:
        employee_number = await self.repository.calculate_employee_number()
        new_employee = EmployeeModel(
            employee_number=employee_number,
            name=employee_data.name,
            surname=employee_data.surname,
            document=employee_data.document,
            entry_date=employee_data.entry_date
        )
        await self.repository.create(new_employee)
        return new_employee

    async def _validate_and_get_positions(self, position_ids: List[int]) -> List[PositionModel]:
        if not position_ids:
            raise ValueError("An employee must have at least one position assigned.")
        positions = await self.position_repository.get_by_ids(position_ids, is_active=True)
        if not positions or len(positions) != len(position_ids):
            raise ValueError("Some positions provided are invalid.")
        if len(positions) > 3:
            raise ValueError("An employee cannot have more than 3 active positions.")
        return positions

    async def _assign_positions_to_employee(self, employee: EmployeeModel, positions: List[PositionModel]):
        for position in positions:
            employee_position = EmployeePosition(
                employee=employee,
                position=position,
                start_date=date.today(),
                end_date=None
            )
            await self.employee_position_repository.create(employee_position)

    def _build_employee_response(self, employee: EmployeeModel, positions: List[PositionModel]) -> Dict:
        return {
            "id": employee.id,
            "employee_number": employee.employee_number,
            "name": employee.name,
            "surname": employee.surname,
            "document": employee.document,
            "entry_date": employee.entry_date,
            "positions": [position.id for position in positions]
        }
    
    async def get_employee(self, employee_id: int) -> Optional[Dict]:
        employee = await self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        return {
            "id": employee.id,
            "employee_number": employee.employee_number,
            "name": employee.name,
            "surname": employee.surname,
            "document": employee.document,
            "entry_date": employee.entry_date,
            "positions": [
                {
                    "position_id": ep.position_id,
                    "start_date": ep.start_date,
                    "end_date": ep.end_date,
                    "is_active": ep.end_date is None
                }
                for ep in employee.employee_positions
            ]
        }
    
    async def update_employee(self, employee_id: int, update_data: EmployeeUpdateDTO)-> EmployeeModel:
       
        employee = await self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        if update_data.name:
            employee.name = update_data.name
        if update_data.surname:
            employee.surname = update_data.surname
            
        await self.repository.update(employee)
        await self.db.refresh(employee)
        return employee
    
    
    async def delete_employee(self, employee_id: int)-> Dict:
        
        employee = await self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        payrolls = await self.payroll_repository.get_by_employee(employee_id)
        for payroll in payrolls:
            await self.payroll_repository.delete(payroll)

        active_positions = await self.employee_position_repository.get_active_relationships(employee_id, [])
        for position in active_positions:
            position.end_date = date.today()

        await self.repository.delete(employee)
        await self.db.commit()
        return {"detail": f"Employee with ID {employee_id} has been deleted."}
    
    
    async def add_positions_to_employee(self, employee_id: int, positions: List[int])-> EmployeeModel:
        employee = await self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        existing_active_positions = {
            ep.position_id
            for ep in employee.employee_positions
            if ep.end_date is None
        }

        active_positions = await self.position_repository.get_by_ids(positions, is_active=True)
        new_positions = [
            position for position in active_positions if position.id not in existing_active_positions
        ]

        if not new_positions:
            raise ValueError("All positions are already assigned to the employee.")

        if len(existing_active_positions) + len(new_positions) > 3:
            raise ValueError("An employee cannot have more than 3 active positions.")

        for position in new_positions:
            employee_position = EmployeePosition(
                employee_id=employee.id,
                position_id=position.id,
                start_date=date.today(),
                end_date=None
            )
            await self.employee_position_repository.create(employee_position)

        await self.db.commit()
        await self.db.refresh(employee)
        return employee
    
    async def remove_positions_from_employee(self, employee_id: int, positions: List[int])-> EmployeeModel:
        employee = await self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        relationships = await self.employee_position_repository.get_active_relationships(employee_id, positions)
        if not relationships:
            raise ValueError("No active relationships found for the given positions.")

        await self.employee_position_repository.update_relationship_end_date(relationships, date.today())

        await self.db.commit()
        await self.db.refresh(employee)
        return employee
    
    
    async def get_position_history(self, employee_id: Optional[int] = None, employee_number: Optional[int] = None)-> List[Dict]:
        if not employee_id and not employee_number:
            raise ValueError("Either employee_id or employee_number must be provided.")

        if employee_id:
            employee = await self.repository.get_by_id(employee_id)
        elif employee_number:
            employee = await self.repository.get_by_employee_number(employee_number)

        if not employee:
            raise ValueError("Employee not found.")

        return [
            {
                "position_id": ep.position_id,
                "start_date": ep.start_date,
                "end_date": ep.end_date,
                "position": {
                    "id": ep.position.id,
                    "description": ep.position.description,
                    "active": ep.position.active
                } if ep.position else None
            }
            for ep in employee.employee_positions
        ]