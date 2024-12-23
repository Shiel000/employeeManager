from sqlalchemy.orm import Session
from app.persistence.orm.models.employee_model import EmployeeModel

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(EmployeeModel).all()

    def get_by_id(self, employee_id: int):
        return self.db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()

    def create(self, employee: EmployeeModel):
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def update(self, employee: EmployeeModel):
        self.db.commit()
        return employee

    def delete(self, employee: EmployeeModel):
        self.db.delete(employee)
        self.db.commit()
