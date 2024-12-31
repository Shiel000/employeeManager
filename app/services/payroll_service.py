from app.dtos.payroll_dto import PayrollCreateDTO, PayrollFilterDTO,PayrollBackupFilterDTO,PayrollReporteFilterDTO,PayrollDeleteFilterDTO,PayrollOutDTO
from app.repositories.employee_position_repository import EmployeePositionRepository
from app.repositories.position_detail_repository import PositionDetailRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.payroll_repository import PayrollRepository
from app.models.payroll_model import PayrollModel
from app.models.employee_model import EmployeeModel
from app.dtos.position_dto import PositionOutDTODTO
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse
from fastapi_pagination import Page,paginate
from collections import defaultdict
from fastapi import UploadFile
from datetime import date
from io import StringIO
import pandas as pd
import csv
import os




class PayrollService:
    def __init__(self, db: AsyncSession, params=None):
        self.db = db
        self.employee_repository = EmployeeRepository(db)
        self.employee_position_repository = EmployeePositionRepository(db)
        self.position_detail_repository = PositionDetailRepository(db)
        self.payroll_repository = PayrollRepository(db)
        self.MINIMUM_WAGE = float(os.getenv("MINIMUM_WAGE"))
        self.params = params

    async def create_payroll(self, payroll_data: PayrollCreateDTO):
        if payroll_data.employee_id:
            employee = await self._validate_employee_exists(payroll_data.employee_id)
            total_salary = await self._calculate_total_salary(employee_id=payroll_data.employee_id)
            seniority_bonus = self._calculate_seniority_bonus(employee, total_salary)
            total_amount = self._calculate_total_amount(total_salary, seniority_bonus)

            payroll = await self._create_or_update_payroll(
                employee_id=payroll_data.employee_id, period=payroll_data.period, total_amount=total_amount
            )
            await self.db.commit()
            await self.db.refresh(payroll)
            await self.db.refresh(employee)
            return await self._build_payroll_response(payroll, employee)
        else:
            
            employees = await self.employee_repository.get_all()
            if not employees:
                raise ValueError("No active employees found.")
            payrolls = []
            for employee in employees:
                total_salary = await self._calculate_total_salary(employee_id=employee.id)
                seniority_bonus = self._calculate_seniority_bonus(employee, total_salary)
                total_amount = self._calculate_total_amount(total_salary, seniority_bonus)
                payroll = await self._create_or_update_payroll(
                    employee_id=employee.id, period=payroll_data.period, total_amount=total_amount
                )
                payrolls.append((payroll, employee))
            await self.db.commit()

            
            details = []
            for payroll, employee in payrolls:
                await self.db.refresh(payroll)  
                await self.db.refresh(employee)  
                details.append(await self._build_payroll_response(payroll, employee))

            return {
                "status": "success",
                "processed_count": len(payrolls),
                "details": details,
            }
    
    
    async def _build_payroll_response(self, payroll: PayrollModel, employee: EmployeeModel) -> PayrollOutDTO:
    
        await self.db.refresh(employee)

        positions = await self.employee_position_repository.get_active_positions_by_employee(employee_id=employee.id)
        position_details = [
            PositionOutDTODTO(id=pos.position_id, description=pos.position.description)
            for pos in positions
        ]
        return PayrollOutDTO(
            id=payroll.id,
            employee_id=payroll.employee_id,
            period=payroll.period,
            amount=payroll.amount,
            employee_name=employee.name,
            employee_surname=employee.surname,
            positions=position_details
        )
    

    async def _validate_employee_exists(self, employee_id: int) -> EmployeeModel:
        employee = await self.employee_repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")
        return employee

    async def _create_or_update_payroll(self, employee_id: int, period: str, total_amount: float) -> PayrollModel:
        payroll = await self.payroll_repository.get_by_employee_and_period(employee_id, period)
        if payroll:
            payroll.amount = total_amount
        else:
            payroll = PayrollModel(
                employee_id=employee_id,
                period=period,
                amount=total_amount
            )
            await self.payroll_repository.create(payroll)
        return payroll

    async def _calculate_total_salary(self, employee_id: int) -> float:
        active_positions = await self.employee_position_repository.get_active_positions_by_employee(employee_id=employee_id)
        total_salary = 0.0
        for position in active_positions:
            detail = await self.position_detail_repository.get_latest_by_position(position.position_id)
            if detail:
                total_salary += detail.salary
        return total_salary

    def _calculate_seniority_bonus(self, employee: EmployeeModel, total_salary: float) -> float:
        years_of_service = date.today().year - employee.entry_date.year
        return total_salary * (years_of_service * 0.01)

    def _calculate_total_amount(self, total_salary: float, seniority_bonus: float) -> float:
        return self.MINIMUM_WAGE + total_salary + seniority_bonus


    async def get_payrolls(self, filters: PayrollFilterDTO) -> Page[PayrollOutDTO]:
        query = await self.payroll_repository.filter_by_params(filters)
        result = await self.db.execute(query)
        payrolls = result.scalars().all()    
        payroll_responses = []
        for payroll in payrolls:
            employee = await self.employee_repository.get_by_id(payroll.employee_id)
            payroll_responses.append(await self._build_payroll_response(payroll, employee))

        return paginate(payroll_responses, self.params)



    async def get_payroll_by_id(self, payroll_id: int) -> PayrollOutDTO:
        payroll = await self.payroll_repository.get_by_id(payroll_id)
        if not payroll:
            raise ValueError("Payroll not found.")

        employee = await self.employee_repository.get_by_id(payroll.employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        return await self._build_payroll_response(payroll, employee)

    async def get_backup_data(self, filters: PayrollBackupFilterDTO):
        query = self.payroll_repository.get_backup_query(filters)
        result = await self.db.execute(query)
        return result.fetchall()

    def generate_csv_backup(self, data):
        grouped_data = defaultdict(lambda: {"positions": [], "position_ids": []})
        for payroll, employee_name, employee_surname, position_id, position_description in data:
            if "id" not in grouped_data[payroll.id]:
                grouped_data[payroll.id].update({
                    "id": payroll.id,
                    "employee_id": payroll.employee_id,
                    "period": payroll.period,
                    "amount": float(payroll.amount),
                    "employee_name": employee_name,
                    "employee_surname": employee_surname,
                })
            if position_description and position_id:
                grouped_data[payroll.id]["positions"].append(position_description)
                grouped_data[payroll.id]["position_ids"].append(position_id)

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Employee ID", "Period", "Amount", "Employee Name", "Employee Surname", "Positions", "Position IDs"])

        for payroll_id, payroll_data in grouped_data.items():
            positions = ", ".join(payroll_data["positions"])
            position_ids = ", ".join(map(str, payroll_data["position_ids"]))
            writer.writerow([
                payroll_data["id"],
                payroll_data["employee_id"],
                payroll_data["period"],
                payroll_data["amount"],
                payroll_data["employee_name"],
                payroll_data["employee_surname"],
                positions,
                position_ids,
            ])

        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={
            "Content-Disposition": "attachment; filename=payroll_backup.csv"
        })
        
    # async def generate_report(self, filters: PayrollReporteFilterDTO):
        # query = self.payroll_repository.get_reports_query(filters)
        # result = await self.db.execute(query)
        # data = result.fetchall()

    #     total_general = sum(row.total_liquidated for row in data)
    #     output = StringIO()
    #     writer = csv.writer(output)
    #     writer.writerow(["Position", "Total Liquidated", "Average per Employee"])

    #     for row in data:
    #         writer.writerow([
    #             row.position_description,
    #             round(float(row.total_liquidated), 2),
    #             round(float(row.average_per_employee), 2)
    #         ])

    #     writer.writerow(["Total", round(total_general, 2), ""])

    #     output.seek(0)
    #     return StreamingResponse(output, media_type="text/csv", headers={
    #         "Content-Disposition": "attachment; filename=payroll_report.csv"
    #     })
    
    async def generate_report(self, filters: PayrollReporteFilterDTO):
        query = self.payroll_repository.get_reports_query(filters)
        data = await self.db.execute(query)
        rows = data.fetchall()

        total_general = sum(row.total_liquidated for row in rows)
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Position",
            "Total Liquidated",
            "Average per Employee",
            "Total Employees",
            "Percentage of Total"
        ])

        for row in rows:
            percentage_of_total = (row.total_liquidated / total_general) * 100
            writer.writerow([
                row.position_description,
                float(row.total_liquidated),
                float(row.average_per_employee),
                row.total_employees,  # Asegúrate de calcular este campo en la query
                round(percentage_of_total, 2),
            ])

        writer.writerow(["Total", total_general, "", "", ""])
        output.seek(0)

        return StreamingResponse(output, media_type="text/csv", headers={
            "Content-Disposition": "attachment; filename=payroll_report.csv"
        })
        
    async def delete_payrolls(self, filters: PayrollDeleteFilterDTO):
        start_date = filters.start_date.strftime("%Y-%m")
        end_date = filters.end_date.strftime("%Y-%m")
        
    
        rows_deleted = await self.payroll_repository.delete_by_filters(
            start_date=start_date,
            end_date=end_date,
            employee_id=filters.employee_id
        )
        await self.db.commit()
        return {"message": f"{rows_deleted} payroll records deleted successfully."}


    async def upload_payroll_csv(self, file: UploadFile, overwrite_existing: bool = False):
        try:
            df = pd.read_csv(file.file)
            column_mapping = {
                "Employee ID": "employee_id",
                "Period": "period",
                "Amount": "amount"
            }
            df.rename(columns=column_mapping, inplace=True)
            required_columns = ["employee_id", "period", "amount"]
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"CSV must contain the following columns: {', '.join(required_columns)}")
            for _, row in df.iterrows():
                await self._process_payroll_row(row, overwrite_existing)
                
            await self.db.commit()
            return {"message": "Payroll data uploaded successfully"}

        except Exception as e:
            raise ValueError(f"Error processing CSV: {e}")

    async def _process_payroll_row(self, row, overwrite_existing: bool):
        employee_id = int(row["employee_id"])
        period = row["period"]
        amount = float(row["amount"])
        existing_payroll = await self.payroll_repository.get_by_employee_and_period(employee_id, period)
        if existing_payroll and not overwrite_existing:
            return 
        elif existing_payroll and overwrite_existing:
            existing_payroll.amount = amount
            await self.payroll_repository.update(existing_payroll)
        else:
            new_payroll = PayrollModel(employee_id=employee_id, period=period, amount=amount)
            await self.payroll_repository.create(new_payroll)
