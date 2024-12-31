from app.dtos.payroll_dto import PayrollCreateDTO,PayrollFilterDTO,PayrollBackupFilterDTO,PayrollReporteFilterDTO,PayrollDeleteFilterDTO,PayrollOutDTO
from app.services.payroll_service import PayrollService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile



class PayrollController:
    def __init__(self, db: AsyncSession, params=None):
        self.service = PayrollService(db, params)
        self.params =params

    async def create_payroll(self, payroll_data: PayrollCreateDTO) -> PayrollOutDTO:
        return await self.service.create_payroll(payroll_data)
    
    async def list_payrolls(self, filters: PayrollFilterDTO):
        return await self.service.get_payrolls(filters)
    
    async def get_payroll(self, payroll_id: int):
        return await self.service.get_payroll_by_id(payroll_id)
    
    async def backup_payroll(self, filters: PayrollBackupFilterDTO):
        data = await self.service.get_backup_data(filters)
        return self.service.generate_csv_backup(data)
    
    async def generate_report(self, filters: PayrollReporteFilterDTO):
        return await self.service.generate_report(filters)

    async def delete_payrolls(self, filters: PayrollDeleteFilterDTO):
        return await self.service.delete_payrolls(filters)
    
    async def upload_payroll_csv(self, file: UploadFile, overwrite_existing: bool = False):
        return await self.service.upload_payroll_csv(file, overwrite_existing)
