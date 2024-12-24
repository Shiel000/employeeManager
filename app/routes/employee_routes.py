from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.controllers.employee_controller import EmployeeController
from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO

router = APIRouter()

@router.get("/")
def get_employees(db: Session = Depends(get_db), include_positions: bool = True):
    controller = EmployeeController(db)
    return controller.get_all_employees(include_positions=include_positions)

@router.get("/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.get_employee(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
def create_employee(employee: EmployeeCreateDTO, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.create_employee(employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeUpdateDTO, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.update_employee(employee_id, employee)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        controller.delete_employee(employee_id)
        return {"detail": "Employee deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
