from sqlalchemy.orm import Session
from app.persistence.repositories.employee_repository import EmployeeRepository
from app.domain.entities.employee import Employee
from app.application.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO
from app.persistence.orm.models.employee_model import EmployeeModel

class EmployeeService:
    def __init__(self, db: Session):
        self.repository = EmployeeRepository(db)

    def get_all_employees(self):
        return self.repository.get_all()

    def get_employee(self, employee_id: int):
        return self.repository.get_by_id(employee_id)

    def create_employee(self, employee_data: EmployeeCreateDTO):
        employee = EmployeeModel(**employee_data.dict())
        return self.repository.create(employee)

    def update_employee(self, employee_id: int, employee_data: EmployeeUpdateDTO):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            return None
        for key, value in employee_data.dict().items():
            setattr(employee, key, value)
        return self.repository.update(employee)

    def delete_employee(self, employee_id: int):
        employee = self.repository.get_by_id(employee_id)
        if employee:
            self.repository.delete(employee)
