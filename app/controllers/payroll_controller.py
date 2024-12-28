from sqlalchemy.orm import Session
from app.services.payroll_service import PayrollService
from app.dtos.payroll_dto import PayrollCreateDTO,PayrollFilterDTO

class PayrollController:
    def __init__(self, db: Session, params= None):
        self.service = PayrollService(db, params)
        self.params =params

    def create_payroll(self, payroll_data: PayrollCreateDTO):
        return self.service.create_payroll(payroll_data)

    def list_payrolls(self, filters: PayrollFilterDTO):
        return self.service.get_payrolls(filters)
    
    def get_payroll(self, payroll_id: int):
        return self.service.get_payroll_by_id(payroll_id)