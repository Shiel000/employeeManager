from sqlalchemy.orm import Session
from app.services.employee_service import EmployeeService
from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO,EmployeeAddDeletePositionsDTO,EmployeeFilter
from typing import Optional


class EmployeeController:
    def __init__(self, db: Session,params=None):
        self.service = EmployeeService(db,params)
        self.params =params                                
        
        
    def get_all_employees(self, filters: Optional[EmployeeFilter], include_positions: bool):
        # Pasa el flag `include_positions` al servicio
        return self.service.get_all_employees(filters, include_positions)


    def create_employee(self, employee_data: EmployeeCreateDTO):
        return self.service.create_employee(employee_data)
    
    def update_employee(self, employee_id: int, update_data: EmployeeUpdateDTO):
        return self.service.update_employee(employee_id, update_data)
    
    def add_positions(self, employee_id: int, positions: EmployeeAddDeletePositionsDTO):
        return self.service.add_positions_to_employee(employee_id, positions.positions)
    
    def remove_positions(self, employee_id: int, positions: EmployeeAddDeletePositionsDTO):
        return self.service.remove_positions_from_employee(employee_id, positions.positions)
    
    def get_position_history(self, employee_id: Optional[int] = None, employee_number: Optional[int] = None):
        return self.service.get_position_history(employee_id=employee_id, employee_number=employee_number)
    
    def get_employee(self, employee_id: int):
        return self.service.get_employee(employee_id)
    
    def delete_employee(self, employee_id: int):
        return self.service.delete_employee(employee_id)
    

    # def get_paginate_employees(self,name: Optional[str],surname: Optional[str],active_position: Optional[bool],page: int,per_page: int,db: Session):
    #     return self.service.paginate_employees(
    #         name=name,
    #         surname=surname,
    #         active_position=active_position,
    #         page=page,
    #         per_page=per_page,
    #         db=db,
    #     )
    
    # def generate_report(self, filters: EmployeeFilter):
    #     return self.service.generate_report(filters=filters)
