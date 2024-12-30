from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.controllers.employee_controller import EmployeeController
from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO,EmployeeAddDeletePositionsDTO, EmployeeFilter,EmployeeOut
from typing import Optional
from fastapi import Query
from fastapi_pagination import Page,Params
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.get("/", response_model=Page[EmployeeOut])
async def get_employees(
    db: AsyncSession = Depends(get_db),  # Cambiar a AsyncSession
    params: Params = Depends(),
    filters: EmployeeFilter = Depends(),
    include_positions: bool = Query(False, description="Include employee positions")
):
    controller = EmployeeController(db, params)
    result = await controller.get_all_employees(filters=filters, include_positions=include_positions)  # Asegurarse de usar await
    return result.dict(exclude_none=True)


@router.post("/")
async def create_employee(employee: EmployeeCreateDTO, db: AsyncSession = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return await controller.create_employee(employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@router.get("/{employee_id}")
async def get_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return await controller.get_employee(employee_id=employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{employee_id}")
async def update_employee(employee_id: int, update_data: EmployeeUpdateDTO, db: AsyncSession = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return await controller.update_employee(employee_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{employee_id}")
async def delete_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return await controller.delete_employee(employee_id=employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/{employee_id}/positions")
async def add_positions(employee_id: int, positions: EmployeeAddDeletePositionsDTO, db: AsyncSession = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return await controller.add_positions(employee_id, positions)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.delete("/{employee_id}/positions")
async def remove_positions(employee_id: int, positions: EmployeeAddDeletePositionsDTO, db: AsyncSession = Depends(get_db)):
    controller = EmployeeController(db)
    try:
        return await controller.remove_positions(employee_id, positions)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.get("/positions/history")
async def get_position_history(
    employee_id: Optional[int] = Query(None),
    employee_number: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    controller = EmployeeController(db)
    try:
        return await controller.get_position_history(employee_id=employee_id, employee_number=employee_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))








# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.models.base import get_db
# from app.controllers.employee_controller import EmployeeController
# from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO,EmployeeAddDeletePositionsDTO, EmployeeFilter,EmployeeOut
# from typing import Optional
# from fastapi import Query
# from fastapi_pagination import Page,Params


# router = APIRouter()


# @router.get("/", response_model=Page[EmployeeOut])
# def get_employees(
#     db: Session = Depends(get_db),
#     params: Params = Depends(),
#     filters: EmployeeFilter = Depends(),
#     include_positions: bool = Query(False, description="Include employee positions")
# ):
#     controller = EmployeeController(db, params)
#     result = controller.get_all_employees(filters=filters, include_positions=include_positions)
#     return result.dict(exclude_none=True)

# @router.post("/")
# def create_employee(employee: EmployeeCreateDTO, db: Session = Depends(get_db)):
#     controller = EmployeeController(db)
#     try:
#         return controller.create_employee(employee)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.get("/{employee_id}")
# def get_employee(employee_id: int, db: Session = Depends(get_db)):
#     controller = EmployeeController(db)
#     try:
#         return controller.get_employee(employee_id=employee_id)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))

    
# @router.put("/{employee_id}")
# def update_employee(employee_id: int, update_data: EmployeeUpdateDTO, db: Session = Depends(get_db)):
#     controller = EmployeeController(db)
#     try:
#         return controller.update_employee(employee_id, update_data)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.delete("/{employee_id}")
# def delete_employee(employee_id: int, db: Session = Depends(get_db)):
#     controller = EmployeeController(db)
#     try:
#         return controller.delete_employee(employee_id=employee_id)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.post("/{employee_id}/positions")
# def add_positions(employee_id: int, positions: EmployeeAddDeletePositionsDTO, db: Session = Depends(get_db)):
#     controller = EmployeeController(db)
#     try:
#         return controller.add_positions(employee_id, positions)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.delete("/{employee_id}/positions")
# def remove_positions(employee_id: int, positions: EmployeeAddDeletePositionsDTO, db: Session = Depends(get_db)):
#     controller = EmployeeController(db)
#     try:
#         return controller.remove_positions(employee_id, positions)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
    
# @router.get("/positions/history")
# def get_position_history(
#     employee_id: Optional[int] = Query(None),
#     employee_number: Optional[int] = Query(None),
#     db: Session = Depends(get_db)):
    
#     controller = EmployeeController(db)
#     try:
#         return controller.get_position_history(employee_id=employee_id, employee_number=employee_number)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
