from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.dtos.payroll_dto import PayrollCreateDTO
from app.controllers.payroll_controller import PayrollController

router = APIRouter()

@router.post("/")
def create_payroll(payroll_data: PayrollCreateDTO, db: Session = Depends(get_db)):
    controller = PayrollController(db)
    try:
        return controller.create_payroll(payroll_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
