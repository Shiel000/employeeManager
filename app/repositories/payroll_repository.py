from sqlalchemy.orm import Session
from app.models.payroll_model import PayrollModel
from typing import  List

class PayrollRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payroll: PayrollModel):
        self.db.add(payroll)
        return payroll
    
    def get_by_employee_and_period(self, employee_id: int, period: str):
        return (
            self.db.query(PayrollModel).filter(PayrollModel.employee_id == employee_id, PayrollModel.period == period).first()
        )