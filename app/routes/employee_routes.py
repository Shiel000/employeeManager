from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.controllers.employee_controller import EmployeeController
from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO,EmployeeAddDeletePositionsDTO
from typing import Optional
from fastapi import Query


router = APIRouter()

@router.post("/")
def create_employee(employee: EmployeeCreateDTO, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.create_employee(employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.put("/{employee_id}")
def update_employee(employee_id: int, update_data: EmployeeUpdateDTO, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.update_employee(employee_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{employee_id}/positions")
def add_positions(employee_id: int, positions: EmployeeAddDeletePositionsDTO, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.add_positions(employee_id, positions)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{employee_id}/positions")
def remove_positions(employee_id: int, positions: EmployeeAddDeletePositionsDTO, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.remove_positions(employee_id, positions)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/positions/history")
def get_position_history(
    employee_id: Optional[int] = Query(None),
    employee_number: Optional[int] = Query(None),
    db: Session = Depends(get_db)):
    
    controller = EmployeeController(db)
    try:
        return controller.get_position_history(employee_id=employee_id, employee_number=employee_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
def list_employees(
    name: Optional[str] = Query(None),
    surname: Optional[str] = Query(None),
    active_position: Optional[bool] = Query(None),  # Parámetro agregado
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Lista empleados con filtros opcionales.
    """
    controller = EmployeeController(db)
    return controller.list_employees(
        name=name, surname=surname, active_position=active_position, skip=skip, limit=limit
    )

@router.get("/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.get_employee(employee_id=employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.delete_employee(employee_id=employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
