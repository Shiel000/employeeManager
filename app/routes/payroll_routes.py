from app.dtos.payroll_dto import PayrollCreateDTO, PayrollFilterDTO,PayrollOutDTO,PayrollBackupFilterDTO,PayrollReporteFilterDTO,PayrollDeleteFilterDTO
from app.controllers.payroll_controller import PayrollController
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page, Params
from fastapi import UploadFile, Query
from app.models.base import get_db
from typing import Dict



router = APIRouter()
    
    
@router.post("/", response_model=Dict)
async def create_payroll(
    payroll_data: PayrollCreateDTO, db: AsyncSession = Depends(get_db)
):
    controller = PayrollController(db)
    result = await controller.create_payroll(payroll_data)

    if isinstance(result, PayrollOutDTO):
        
        return {
            "status": "success",
            "processed_count": 1,
            "data": result.dict(exclude_none=True)
        }
    else:
        return {
            "status": "success",
            "processed_count": len(result["details"]),
            "data": [payroll.dict(exclude_none=True) for payroll in result["details"]]
        }
    
@router.get("/", response_model=Page[PayrollOutDTO])
async def list_payrolls(
    filters: PayrollFilterDTO = Depends(),
    params: Params = Depends(),
    db: AsyncSession = Depends(get_db)
):
    controller = PayrollController(db, params)
    return await controller.list_payrolls(filters)


@router.get("/{payroll_id}")
async def get_payroll(payroll_id: int, db: AsyncSession = Depends(get_db)):
    controller = PayrollController(db)
    try:
        payroll = await controller.get_payroll(payroll_id)
        return payroll
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/operations/backup", response_class=StreamingResponse)
async def backup_payroll(
    filters: PayrollBackupFilterDTO = Depends(),
    db: AsyncSession = Depends(get_db)
):
    controller = PayrollController(db)
    try:
        return await controller.backup_payroll(filters)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/operations/reports", response_class=StreamingResponse)
async def generate_report(
    filters: PayrollReporteFilterDTO = Depends(),
    db: AsyncSession = Depends(get_db)
):
    controller = PayrollController(db)
    return await controller.generate_report(filters)

@router.delete("/operations/delete")
async def delete_payrolls(
    filters: PayrollDeleteFilterDTO = Depends(),
    db: AsyncSession = Depends(get_db)
):
    controller = PayrollController(db)
    return await controller.delete_payrolls(filters)


@router.post("/operations/upload")
async def upload_payroll_csv(
    file: UploadFile,
    overwrite_existing: bool = Query(False, description="Overwrite existing payroll records"),
    db: AsyncSession = Depends(get_db)
):
    controller = PayrollController(db)
    return await controller.upload_payroll_csv(file, overwrite_existing)
