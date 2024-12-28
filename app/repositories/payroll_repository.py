from sqlalchemy.orm import Session
from app.models.payroll_model import PayrollModel
from app.dtos.payroll_dto import PayrollFilterDTO, PayrollBackupFilterDTO,PayrollReporteFilterDTO
from app.models.employee_position_table import EmployeePosition
from app.models.employee_model import EmployeeModel
from app.models.position_model import PositionModel
from typing import  Optional
from sqlalchemy.orm import Query
from sqlalchemy.sql import func


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
        
        
        
        
    def get_backup_query(self, filters: PayrollBackupFilterDTO) -> Query:
        query = (
            self.db.query(
                PayrollModel,
                EmployeeModel.name.label("employee_name"),
                EmployeeModel.surname.label("employee_surname"),
                PositionModel.id.label("position_id"),
                PositionModel.description.label("position_description")
            )
            .join(EmployeeModel, PayrollModel.employee_id == EmployeeModel.id)
            .join(EmployeePosition, EmployeePosition.employee_id == EmployeeModel.id, isouter=True)
            .join(PositionModel, EmployeePosition.position_id == PositionModel.id, isouter=True)
        )

        # Aplica filtros
        if filters.start_date:
            query = query.filter(PayrollModel.period >= filters.start_date.strftime("%Y-%m"))
        if filters.end_date:
            query = query.filter(PayrollModel.period <= filters.end_date.strftime("%Y-%m"))
        if filters.employee_id:
            query = query.filter(PayrollModel.employee_id == filters.employee_id)

        return query
    
    def get_reports_query(self, filters: PayrollReporteFilterDTO) -> Query:
        query = (
            self.db.query(
                PositionModel.description.label("position_description"),
                func.sum(PayrollModel.amount).label("total_liquidated"),
                func.avg(PayrollModel.amount).label("average_per_employee")
            )
            .join(EmployeeModel, PayrollModel.employee_id == EmployeeModel.id)
            .join(EmployeePosition, EmployeePosition.employee_id == EmployeeModel.id)
            .join(PositionModel, EmployeePosition.position_id == PositionModel.id)
            .group_by(PositionModel.id, PositionModel.description)
        )

        # Aplica filtros
        if filters.start_date:
            query = query.filter(PayrollModel.period >= filters.start_date.strftime("%Y-%m"))
        if filters.end_date:
            query = query.filter(PayrollModel.period <= filters.end_date.strftime("%Y-%m"))
        if filters.position_id:
            query = query.filter(PositionModel.id == filters.position_id)
        if filters.employee_id:  # Nuevo filtro para empleado
            query = query.filter(PayrollModel.employee_id == filters.employee_id)

        return query
    
    
    def delete_by_filters(self, start_date: str, end_date: str, employee_id: Optional[int] = None):
        query = self.db.query(PayrollModel).filter(
            PayrollModel.period >= start_date,
            PayrollModel.period <= end_date
        )
        if employee_id:
            query = query.filter(PayrollModel.employee_id == employee_id)

        # Eliminar las filas seleccionadas
        rows_deleted = query.delete(synchronize_session=False)
        return rows_deleted
    
    
    
    
    # def get_reports_query(self, filters: PayrollBackupFilterDTO) -> Query:
    #     query = (
    #         self.db.query(
    #             PositionModel.description.label("position_description"),
    #             func.sum(PayrollModel.amount).label("total_liquidated"),
    #             func.avg(PayrollModel.amount).label("average_per_employee")
    #         )
    #         .join(EmployeeModel, PayrollModel.employee_id == EmployeeModel.id)
    #         .join(EmployeePosition, EmployeePosition.employee_id == EmployeeModel.id)
    #         .join(PositionModel, EmployeePosition.position_id == PositionModel.id)
    #         .group_by(PositionModel.id, PositionModel.description)
    #     )

    #     # Aplica filtros
    #     if filters.start_date:
    #         query = query.filter(PayrollModel.period >= filters.start_date.strftime("%Y-%m"))
    #     if filters.end_date:
    #         query = query.filter(PayrollModel.period <= filters.end_date.strftime("%Y-%m"))
    #     if filters.position_id:
    #         query = query.filter(PositionModel.id == filters.position_id)

    #     return query
        
        
        
        
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
    