from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.controllers.employee_controller import EmployeeController
from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO,EmployeeAddDeletePositionsDTO, EmployeeFilter,EmployeeOut
from typing import Optional
from fastapi import Query
from fastapi_pagination import Page, add_pagination, paginate, Params


router = APIRouter()


@router.get("/", response_model=Page[EmployeeOut])
def get_employees(
    db: Session = Depends(get_db),
    params: Params = Depends(),
    filters: EmployeeFilter = Depends(),
    include_positions: bool = Query(False, description="Include employee positions")
):
    controller = EmployeeController(db, params)
    result = controller.get_all_employees(filters=filters, include_positions=include_positions)
    return result.dict(exclude_none=True)

@router.post("/")
def create_employee(employee: EmployeeCreateDTO, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.create_employee(employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.get_employee(employee_id=employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    
@router.put("/{employee_id}")
def update_employee(employee_id: int, update_data: EmployeeUpdateDTO, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.update_employee(employee_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return controller.delete_employee(employee_id=employee_id)
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


# @router.get("/report")
# def generate_employee_report(
#     db: Session = Depends(get_db),
#     filters: EmployeeFilter = Depends()
# ):
#     controller = EmployeeController(db)
#     try:
#         return controller.generate_report(filters=filters)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))












# @router.get("/", response_model=EmployeeOut)
# def list_employees(
#     filters: EmployeeFilter = Depends(),
#     page: int = Query(1, ge=1, description="Page number"),
#     per_page: int = Query(10, ge=1, le=100, description="Page items"),
#     db: Session = Depends(get_db),
# ):
#     controller = EmployeeController(db)
#     return controller.get_paginate_employees(
#         name=filters.name,
#         surname=filters.surname,
#         active_position=filters.active_position,
#         page=page,
#         per_page=per_page,
#         db=db,
#     )

















# @router.get("/")
# def list_employees(
#     name: Optional[str] = Query(None),
#     surname: Optional[str] = Query(None),
#     active_position: Optional[bool] = Query(None),  # Parámetro agregado
#     skip: int = Query(0, ge=0),
#     limit: int = Query(10, ge=1, le=100),
#     db: Session = Depends(get_db)
# ):
#     """
#     Lista empleados con filtros opcionales.
#     """
#     controller = EmployeeController(db)
#     return controller.list_employees(
#         name=name, surname=surname, active_position=active_position, skip=skip, limit=limit
#     )

# @router.get("/")
# def list_employees(
#     filters: EmployeeFilter = Depends(),  # Usando el DTO desde la carpeta `dtos`
#     db: Session = Depends(get_db)
# ):
#     controller = EmployeeController(db)
#     return controller.list_employees(
#         name=filters.name,
#         surname=filters.surname,
#         active_position=filters.active_position,
#         skip=filters.skip,
#         limit=filters.limit
#     )




# @router.get("/", response_model=EmployeeOut)
# def list_employees(
#     filters: EmployeeFilter = Depends(),
#     page: int = Query(1, ge=1, description="Page number"),
#     per_page: int = Query(10, ge=1, le=100, description="Page items"),
#     db: Session = Depends(get_db),
# ):
#     controller = EmployeeController(db)
#     return controller.get_paginate_employees(
#         name=filters.name,
#         surname=filters.surname,
#         active_position=filters.active_position,
#         page=page,
#         per_page=per_page,
#         db=db,
#     )

# @router.get("/u",response_model=Page[EmployeeOut])
# def get_employees(
#     db: Session = Depends(get_db),
#     params:Params=Depends(),
#     filters: EmployeeFilter = Depends()):
#     controller = EmployeeController(db,params)
#     return controller.get_all_employees(filters=filters)

# @router.get("/u", response_model=Page[EmployeeOut])
# def get_employees(
#     db: Session = Depends(get_db),
#     params: Params = Depends(),
#     filters: EmployeeFilter = Depends(),
#     include_positions: bool = Query(False, description="Include employee positions")
# ):
#     controller = EmployeeController(db, params)
#     return controller.get_all_employees(filters=filters, include_positions=include_positions)