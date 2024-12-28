from sqlalchemy.orm import Session
from app.services.payroll_service import PayrollService
from app.dtos.payroll_dto import PayrollCreateDTO,PayrollFilterDTO,PayrollBackupFilterDTO,PayrollReporteFilterDTO,PayrollDeleteFilterDTO
from fastapi import UploadFile


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
    
    def backup_payroll(self, filters: PayrollBackupFilterDTO):
        data = self.service.get_backup_data(filters)
        return self.service.generate_csv_backup(data) 
    
    def generate_report(self, filters: PayrollReporteFilterDTO):
        return self.service.generate_report(filters)
    
    def delete_payrolls(self, filters: PayrollDeleteFilterDTO):
        return self.service.delete_payrolls(filters)
    
    def upload_payroll_csv(self, file: UploadFile, overwrite_existing: bool = False):
        return self.service.upload_payroll_csv(file, overwrite_existing)