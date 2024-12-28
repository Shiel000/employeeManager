from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.dtos.payroll_dto import PayrollCreateDTO, PayrollFilterDTO,PayrollOutDTO,PayrollBackupFilterDTO,PayrollReporteFilterDTO,PayrollDeleteFilterDTO
from app.controllers.payroll_controller import PayrollController
from fastapi_pagination import Page, Params
router = APIRouter()
from fastapi.responses import StreamingResponse
from fastapi import UploadFile, Query

@router.post("/")
def create_payroll(payroll_data: PayrollCreateDTO, db: Session = Depends(get_db)):
    controller = PayrollController(db)
    try:
        return controller.create_payroll(payroll_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/", response_model=Page[PayrollOutDTO])
def list_payrolls(
    filters: PayrollFilterDTO = Depends(),
    params: Params = Depends(),
    db: Session = Depends(get_db)
):
    controller = PayrollController(db, params)
    return controller.list_payrolls(filters)

@router.get("/{payroll_id}", response_model=PayrollOutDTO)
def get_payroll(payroll_id: int, db: Session = Depends(get_db)):
    controller = PayrollController(db)
    return controller.get_payroll(payroll_id)


@router.get("/operations/backup", response_class=StreamingResponse)
def backup_payroll(
    filters: PayrollBackupFilterDTO = Depends(),
    db: Session = Depends(get_db)
):
    controller = PayrollController(db)
    return controller.backup_payroll(filters)

@router.get("/operations/reports", response_class=StreamingResponse)
def generate_report(
    filters: PayrollReporteFilterDTO = Depends(),
    db: Session = Depends(get_db)
):
    controller = PayrollController(db)
    return controller.generate_report(filters)

@router.delete("/operations/delete")
def delete_payrolls(
    filters: PayrollDeleteFilterDTO = Depends(),
    db: Session = Depends(get_db)
):
    controller = PayrollController(db)
    return controller.delete_payrolls(filters)

@router.post("/operations/upload")
def upload_payroll_csv(
    file: UploadFile,
    overwrite_existing: bool = Query(False, description="Overwrite existing payroll records"),
    db: Session = Depends(get_db)
):
    controller = PayrollController(db)
    return controller.upload_payroll_csv(file, overwrite_existing)