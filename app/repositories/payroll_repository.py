from app.dtos.payroll_dto import PayrollFilterDTO, PayrollBackupFilterDTO,PayrollReporteFilterDTO
from app.models.employee_position_table import EmployeePosition
from app.models.payroll_model import PayrollModel
from app.models.employee_model import EmployeeModel
from app.models.position_model import PositionModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Query
from sqlalchemy.sql import func
from sqlalchemy import delete
from typing import  Optional
from sqlalchemy.sql.expression import distinct


class PayrollRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_employee(self, employee_id: int):
        query = select(PayrollModel).where(PayrollModel.employee_id == employee_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def delete(self, payroll: PayrollModel):
        await self.db.delete(payroll)
        
    async def get_by_employee_and_period(self, employee_id: int, period: str) -> Optional[PayrollModel]:
        query = (
            select(PayrollModel)
            .where(PayrollModel.employee_id == employee_id, PayrollModel.period == period)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, payroll: PayrollModel) -> None:
        self.db.add(payroll)
        
    
    async def update(self, payroll: PayrollModel):
        self.db.add(payroll)


    async def filter_by_params(self, filters: Optional[PayrollFilterDTO]) -> Query:
        query = (
            select(PayrollModel)
            .distinct(PayrollModel.id)
            .select_from(PayrollModel)
            .join(EmployeePosition, EmployeePosition.employee_id == PayrollModel.employee_id)
            .join(PositionModel, EmployeePosition.position_id == PositionModel.id)
        )
        if filters.employee_id:
            query = query.where(PayrollModel.employee_id == filters.employee_id)
        if filters.position_id:
            query = query.where(EmployeePosition.position_id == filters.position_id)
        if filters.start_date:
            query = query.where(PayrollModel.period >= filters.start_date.strftime("%Y-%m"))
        if filters.end_date:
            query = query.where(PayrollModel.period <= filters.end_date.strftime("%Y-%m"))
        return query


    async def get_by_id(self, payroll_id: int) -> Optional[PayrollModel]:
        query = select(PayrollModel).where(PayrollModel.id == payroll_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    def get_backup_query(self, filters: PayrollBackupFilterDTO):
        query = (
            select(
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

        if filters.start_date:
            query = query.where(PayrollModel.period >= filters.start_date.strftime("%Y-%m"))
        if filters.end_date:
            query = query.where(PayrollModel.period <= filters.end_date.strftime("%Y-%m"))
        if filters.employee_id:
            query = query.where(PayrollModel.employee_id == filters.employee_id)

        return query
    
    # def get_reports_query(self, filters: PayrollReporteFilterDTO):
    #     query = (
    #         select(
    #             PositionModel.description.label("position_description"),
    #             func.sum(PayrollModel.amount).label("total_liquidated"),
    #             func.avg(PayrollModel.amount).label("average_per_employee")
    #         )
    #         .join(EmployeePosition, EmployeePosition.position_id == PositionModel.id, isouter=True)
    #         .join(PayrollModel, EmployeePosition.employee_id == PayrollModel.employee_id, isouter=True)
    #         .group_by(PositionModel.description)
    #     )

        
    #     if filters.start_date:
    #         query = query.where(PayrollModel.period >= filters.start_date.strftime("%Y-%m"))
    #     if filters.end_date:
    #         query = query.where(PayrollModel.period <= filters.end_date.strftime("%Y-%m"))
    #     if filters.position_id:
    #         query = query.where(PositionModel.id == filters.position_id)

    #     return query
    
    def get_reports_query(self, filters: PayrollReporteFilterDTO) -> Query:
        query = (
            select(
                PositionModel.description.label("position_description"),
                func.sum(PayrollModel.amount).label("total_liquidated"),
                func.avg(PayrollModel.amount).label("average_per_employee"),
                func.count(distinct(PayrollModel.employee_id)).label("total_employees")
            )
            .select_from(PositionModel)
            .join(EmployeePosition, EmployeePosition.position_id == PositionModel.id, isouter=True)
            .join(PayrollModel, PayrollModel.employee_id == EmployeePosition.employee_id, isouter=True)
            .group_by(PositionModel.id, PositionModel.description)
        )

    # Aplica filtros opcionales
        if filters.start_date:
            query = query.filter(PayrollModel.period >= filters.start_date.strftime("%Y-%m"))
        if filters.end_date:
            query = query.filter(PayrollModel.period <= filters.end_date.strftime("%Y-%m"))
        if filters.employee_id:
            query = query.filter(PayrollModel.employee_id == filters.employee_id)

        return query
    
    async def delete_by_filters(self, start_date: str, end_date: str, employee_id: Optional[int] = None):
        query = (
            delete(PayrollModel)
            .where(
                PayrollModel.period >= start_date,
                PayrollModel.period <= end_date
            )
        )
        if employee_id:
            query = query.where(PayrollModel.employee_id == employee_id)
        result = await self.db.execute(query)
        return result.rowcount
