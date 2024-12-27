from sqlalchemy.orm import Session
from app.models.employee_model import EmployeeModel
from app.models.employee_position_table import EmployeePosition
from app.models.position_model import PositionModel
from typing import List
from sqlalchemy.orm import Query
from typing import List, Optional
from app.dtos.employee_dto import EmployeeFilter
from sqlalchemy.orm import joinedload


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
    


    def filter_by_params(self, filters:Optional[EmployeeFilter]) -> Query:
        
        query = self.db.query(EmployeeModel).join(EmployeePosition)

        if filters.name:
            query = query.filter(EmployeeModel.name.ilike(f"%{filters.name}%"))
        
        if filters.surname:
            query = query.filter(EmployeeModel.surname.ilike(f"%{filters.surname}%"))
            
        if filters.position is not None :
            query = query.filter(EmployeePosition.position_id == filters.position)
        # print(query) 
        return query
    
    def get_employee_positions(self, employee_id: int) -> List[EmployeePosition]:
        return self.db.query(EmployeePosition).join(PositionModel).filter(EmployeePosition.employee_id == employee_id).all()
    
    # def filter_by_params(self, filters: Optional[EmployeeFilter]) -> Query:
    #     # Carga los datos con las relaciones necesarias
    #     query = self.db.query(EmployeeModel).options(
    #         joinedload(EmployeeModel.employee_positions).joinedload(EmployeePosition.position)
    #     )

    #     # Filtros opcionales
    #     if filters.name:
    #         query = query.filter(EmployeeModel.name.ilike(f"%{filters.name}%"))
    #     if filters.surname:
    #         query = query.filter(EmployeeModel.surname.ilike(f"%{filters.surname}%"))
    #     if filters.position is not None:
    #         query = query.join(EmployeePosition).filter(EmployeePosition.position_id == filters.position)

    #     return query