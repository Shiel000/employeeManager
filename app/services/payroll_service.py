from app.dtos.payroll_dto import PayrollCreateDTO, PayrollFilterDTO,PayrollBackupFilterDTO,PayrollReporteFilterDTO,PayrollDeleteFilterDTO
from app.repositories.employee_position_repository import EmployeePositionRepository
from app.repositories.position_detail_repository import PositionDetailRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.payroll_repository import PayrollRepository
from app.models.payroll_model import PayrollModel
from fastapi.responses import StreamingResponse
from fastapi_pagination import paginate
from sqlalchemy.orm import Session
from collections import defaultdict
from io import StringIO
from datetime import date
import pandas as pd
import csv
import os



class PayrollService:
    def __init__(self, db: Session, params=None):
        self.db = db
        self.employee_repository = EmployeeRepository(db)
        self.employee_position_repository = EmployeePositionRepository(db)
        self.position_detail_repository = PositionDetailRepository(db)
        self.payroll_repository = PayrollRepository(db)
        self.MINIMUM_WAGE = float(os.getenv("MINIMUM_WAGE"))
        self.params = params
        

        
    def get_payrolls(self, filters: PayrollFilterDTO):
        query = self.payroll_repository.filter_by_params(filters).all()
        payrolls = self._group_payroll_data(query)
        return paginate(payrolls, self.params)
        
    def get_payroll_by_id(self, payroll_id: int):
        query_results = self.payroll_repository.get_by_id(payroll_id)
        if not query_results:
            raise ValueError("Payroll not found.")
        payrolls = self._group_payroll_data(query_results)
        return payrolls[0] 
        
    def _group_payroll_data(self, query_results):
        grouped_data = defaultdict(lambda: {"positions": []})
        for payroll, employee, position in query_results:
            if payroll.id not in grouped_data:
                grouped_data[payroll.id] = {
                    "id": payroll.id,
                    "employee_id": payroll.employee_id,
                    "period": payroll.period,
                    "amount": float(payroll.amount),
                    "employee_name": employee.name,
                    "employee_surname": employee.surname,
                    "positions": []
                }
            if position:
                grouped_data[payroll.id]["positions"].append({
                    "position_id": position.id,
                    "position_description": position.description
                })
        return list(grouped_data.values())
        
    
    
    def create_payroll(self, payroll_data: PayrollCreateDTO):

        employee = self._validate_employee_exists(payroll_data.employee_id)
        
        total_salary = self._calculate_total_salary(employee_id=payroll_data.employee_id)
        seniority_bonus = self._calculate_seniority_bonus(employee, total_salary)
        total_amount = self._calculate_total_amount(total_salary, seniority_bonus)

        payroll = self._create_or_update_payroll(
            employee_id=payroll_data.employee_id, period=payroll_data.period, total_amount=total_amount
        )

        self.db.commit()
        return self._build_payroll_response(payroll)
    
    
    
    def _validate_employee_exists(self, employee_id: int):
        employee = self.employee_repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")
        return employee

    def _create_or_update_payroll(self, employee_id: int, period: str, total_amount: float):
        payroll = self.payroll_repository.get_by_employee_and_period(employee_id, period)
        if payroll:
            payroll.amount = total_amount
        else:
            payroll = PayrollModel(
                employee_id=employee_id,
                period=period,
                amount=total_amount
            )
            self.payroll_repository.create(payroll)
        return payroll
        
        
    def _calculate_total_salary(self, employee_id: int):
        active_positions = self.employee_position_repository.get_active_positions_by_employee(employee_id=employee_id)
        total_salary = 0.0
        for position in active_positions:
            detail = self.position_detail_repository.get_latest_by_position(position.position_id)
            if detail:
                total_salary += detail.salary
        return total_salary

    def _calculate_seniority_bonus(self, employee, total_salary: float):
        years_of_service = date.today().year - employee.entry_date.year
        return total_salary * (years_of_service * 0.01)

    def _calculate_total_amount(self, total_salary: float, seniority_bonus: float):
        return self.MINIMUM_WAGE + total_salary + seniority_bonus
    
    
    def _create_payroll_record(self, employee_id: int, period: str, total_amount: float):
        payroll = PayrollModel(
            employee_id=employee_id,
            period=period,
            amount=total_amount
        )
        self.payroll_repository.create(payroll)
        return payroll

    def _build_payroll_response(self, payroll: PayrollModel):
        return {
            "employee_id": payroll.employee_id,
            "period": payroll.period,
            "amount": payroll.amount
        }

    def get_backup_data(self, filters: PayrollBackupFilterDTO):
        query = self.payroll_repository.filter_by_params(filters)
        return query.all()

   

    def get_backup_data(self, filters: PayrollBackupFilterDTO):
        query = self.payroll_repository.get_backup_query(filters)
        return query.all()
    

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
        
    def generate_report(self, filters: PayrollReporteFilterDTO):
    
        query = self.payroll_repository.get_reports_query(filters)
        data = query.all()

        total_general = sum(row.total_liquidated for row in data)
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Position", "Total Liquidated", "Average per Employee"])

        for row in data:
            writer.writerow([
                row.position_description,
                float(row.total_liquidated),
                float(row.average_per_employee)
            ])

        writer.writerow(["Total", total_general, ""])

        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={
            "Content-Disposition": "attachment; filename=payroll_report.csv"
        })
        
    def delete_payrolls(self, filters: PayrollDeleteFilterDTO):
        start_date = filters.start_date.strftime("%Y-%m")
        end_date = filters.end_date.strftime("%Y-%m")
        
        # Llama al repositorio para realizar la eliminación
        rows_deleted = self.payroll_repository.delete_by_filters(
            start_date=start_date,
            end_date=end_date,
            employee_id=filters.employee_id
        )

        self.db.commit()
        return {"message": f"{rows_deleted} payroll records deleted successfully."}
    
    

    def upload_payroll_csv(self,file, overwrite_existing=False):
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
                self._process_payroll_row(row, overwrite_existing)
                
            self.db.commit()
            return {"message": "Payroll data uploaded successfully"}

        except Exception as e:
            raise ValueError(f"Error processing CSV: {e}")

    def _process_payroll_row(self,row, overwrite_existing):
        employee_id = int(row["employee_id"])
        period = row["period"]
        amount = float(row["amount"])
        existing_payroll = self.payroll_repository.get_by_employee_and_period(employee_id, period)
        if existing_payroll and not overwrite_existing:
            return  # Ignor
        elif existing_payroll and overwrite_existing:
            existing_payroll.amount = amount
            self.payroll_repository.update(existing_payroll)
        else:
            
            new_payroll = PayrollModel(employee_id=employee_id, period=period, amount=amount)
            self.payroll_repository.create(new_payroll)
