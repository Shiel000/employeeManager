from sqlalchemy.orm import Session
from app.application.services.employee_service import EmployeeService
from app.application.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO

class EmployeeController:
    def __init__(self, db: Session):
        self.service = EmployeeService(db)

    def get_all_employees(self, include_positions: bool = True):
        employees = self.service.get_all_employees()
        # Lógica específica de presentación: filtrar datos relacionados (por ejemplo, posiciones)
        if not include_positions:
            for employee in employees:
                employee.positions = []  # Excluir las posiciones de la respuesta
        return employees

    def get_employee(self, employee_id: int):
        employee = self.service.get_employee(employee_id)
        if not employee:
            raise ValueError("Employee not found")
        return employee

    def create_employee(self, employee_data: EmployeeCreateDTO):
        # Validación específica (si es necesario)
        if len(employee_data.legajo) > 10:
            raise ValueError("Legajo cannot exceed 10 characters")
        return self.service.create_employee(employee_data)

    def update_employee(self, employee_id: int, employee_data: EmployeeUpdateDTO):
        employee = self.service.get_employee(employee_id)
        if not employee:
            raise ValueError("Employee not found")
        return self.service.update_employee(employee_id, employee_data)

    def delete_employee(self, employee_id: int):
        employee = self.service.get_employee(employee_id)
        if not employee:
            raise ValueError("Employee not found")
        self.servic
