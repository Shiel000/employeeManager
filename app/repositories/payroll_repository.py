from sqlalchemy.orm import Session
from app.models.payroll_model import PayrollModel
from app.dtos.payroll_dto import PayrollFilterDTO
from app.models.employee_position_table import EmployeePosition
from app.models.employee_model import EmployeeModel
from app.models.position_model import PositionModel
from typing import  Optional
from sqlalchemy.orm import Query

class PayrollRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payroll: PayrollModel):
        self.db.add(payroll)
        return payroll
    
    def get_by_employee(self, employee_id: int):
        return self.db.query(PayrollModel).filter(PayrollModel.employee_id == employee_id).all()

    def delete(self, payroll: PayrollModel):
        self.db.delete(payroll)
        
        
        
    def get_by_employee_and_period(self, employee_id: int, period: str):
        return (
            self.db.query(PayrollModel).filter(PayrollModel.employee_id == employee_id, PayrollModel.period == period).first()
        )
        
    
    def filter_by_params(self, filters: Optional[PayrollFilterDTO])->Query:
        query = (
            self.db.query(PayrollModel,EmployeeModel,PositionModel)
            .join(EmployeeModel, PayrollModel.employee_id == EmployeeModel.id)
            .join(EmployeePosition, EmployeePosition.employee_id == PayrollModel.employee_id, isouter=True)
            .join(PositionModel, EmployeePosition.position_id == PositionModel.id, isouter=True)
        )

        # Filtros
        if filters.employee_id:
            query = query.filter(PayrollModel.employee_id == filters.employee_id)
        if filters.position_id:
            query = query.filter(EmployeePosition.position_id == filters.position_id)
        if filters.start_date:
            query = query.filter(PayrollModel.period >= filters.start_date.strftime("%Y-%m"))
        if filters.end_date:
            query = query.filter(PayrollModel.period <= filters.end_date.strftime("%Y-%m"))

        return query
    
    def get_by_id(self, payroll_id: int):
        return (
            self.db.query(PayrollModel, EmployeeModel, PositionModel)
            .join(EmployeeModel, PayrollModel.employee_id == EmployeeModel.id)
            .join(EmployeePosition, EmployeePosition.employee_id == PayrollModel.employee_id, isouter=True)
            .join(PositionModel, EmployeePosition.position_id == PositionModel.id, isouter=True)
            .filter(PayrollModel.id == payroll_id)
            .all()  # Devuelve una lista de tuplas (PayrollModel, EmployeeModel, PositionModel)
        )
        
        
        
        
        
        
        
        
        
        # def filter_by_params(self, filters: Optional[PayrollFilterDTO])->Query:
        
    #         query = self.db.query(PayrollModel)

    #         if filters.employee_id:
    #             query = query.filter(PayrollModel.employee_id == filters.employee_id)

    #         if filters.position_id:
    #             query = query.join(EmployeePosition).filter(EmployeePosition.position_id == filters.position_id)

    #         if filters.start_date:
    #             query = query.filter(PayrollModel.period >= filters.start_date.strftime("%Y-%m"))
    #         if filters.end_date:
    #             query = query.filter(PayrollModel.period <= filters.end_date.strftime("%Y-%m"))

    #         return query
    