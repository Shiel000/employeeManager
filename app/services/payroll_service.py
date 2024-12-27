from app.repositories.employee_repository import EmployeeRepository
from app.repositories.employee_position_repository import EmployeePositionRepository
from app.repositories.position_detail_repository import PositionDetailRepository
from app.repositories.payroll_repository import PayrollRepository
from sqlalchemy.orm import Session
from app.dtos.payroll_dto import PayrollCreateDTO
from datetime import date
from app.models.payroll_model import PayrollModel
import os

class PayrollService:
    def __init__(self, db: Session):
        self.db = db
        self.employee_repository = EmployeeRepository(db)
        self.employee_position_repository = EmployeePositionRepository(db)
        self.position_detail_repository = PositionDetailRepository(db)
        self.payroll_repository = PayrollRepository(db)
        self.MINIMUM_WAGE = float(os.getenv("MINIMUM_WAGE", "1000.00"))



    # def get_all_employees(self, filters: Optional[EmployeeFilter], include_positions: bool):
    #     query = self.repository.filter_by_params(filters)
    #     query= query.all()
    #     paginated_data = paginate(query, self.params)


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
            # Actualizar el registro existente
            payroll.amount = total_amount
        else:
            # Crear un nuevo registro
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





