from sqlalchemy.orm import Session
from app.models.employee_model import EmployeeModel
from app.models.employee_position_table import EmployeePosition
from typing import List

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(EmployeeModel).all()

    def get_by_id(self, employee_id: int):
        return self.db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()

    def create(self, employee: EmployeeModel):
        self.db.add(employee)
        return employee

    def update(self, employee: EmployeeModel):
        self.db.commit()
        return employee

    def delete(self, employee: EmployeeModel):
        self.db.delete(employee)
        self.db.commit()

    def get_by_document(self, document: int):
        return self.db.query(EmployeeModel).filter(EmployeeModel.document == document).first()

    def get_last_employee(self):
        return self.db.query(EmployeeModel).order_by(EmployeeModel.employee_number.desc()).first()

    def get_by_employee_number(self,employee_number):
        return self.db.query(EmployeeModel).filter(EmployeeModel.employee_number == employee_number).first()
    
    
    def list_employees(self, filters: dict, skip: int, limit: int):
        """
        Lista empleados aplicando filtros opcionales, paginación y ordenación.
        """
        query = self.db.query(EmployeeModel).join(EmployeePosition)

        if "name" in filters:
            query = query.filter(EmployeeModel.name.ilike(f"%{filters['name']}%"))
        if "surname" in filters:
            query = query.filter(EmployeeModel.surname.ilike(f"%{filters['surname']}%"))
        if "active_position" in filters and filters["active_position"]:
            query = query.filter(EmployeePosition.end_date == None)  # Solo posiciones activas

        return query.offset(skip).limit(limit).all()
    
    def delete(self, employee: EmployeeModel):
        self.db.delete(employee)
        
    def get_active_relationships(self, employee_id: int, position_ids: List[int]):
        query = self.db.query(EmployeePosition).filter(
            EmployeePosition.employee_id == employee_id,
            EmployeePosition.end_date == None
        )
        if position_ids:
            query = query.filter(EmployeePosition.position_id.in_(position_ids))
        return query.all()