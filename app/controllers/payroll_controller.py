from sqlalchemy.orm import Session
from app.services.payroll_service import PayrollService
from app.dtos.payroll_dto import PayrollCreateDTO

class PayrollController:
    def __init__(self, db: Session):
        self.service = PayrollService(db)

    def create_payroll(self, payroll_data: PayrollCreateDTO):
        return self.service.create_payroll(payroll_data)
