from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import SessionLocal
from app.services.employee_service import EmployeeService
from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO

router = APIRouter()

# Dependency to provide a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_employees(db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.get_all_employees()

@router.get("/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    employee = service.get_employee(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.post("/")
def create_employee(employee: EmployeeCreateDTO, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    return service.create_employee(employee)

@router.put("/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeUpdateDTO, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    updated_employee = service.update_employee(employee_id, employee)
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    service = EmployeeService(db)
    service.delete_employee(employee_id)
    return {"detail": "Employee deleted"}
