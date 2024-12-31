from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO,EmployeeAddDeletePositionsDTO, EmployeeFilter,EmployeeOutDRO
from app.controllers.employee_controller import EmployeeController
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page,Params
from app.models.base import get_db
from typing import Optional
from fastapi import Query




router = APIRouter()

@router.get("/", response_model=Page[EmployeeOutDRO])
async def get_employees(
    db: AsyncSession = Depends(get_db),
    params: Params = Depends(),
    filters: EmployeeFilter = Depends(),
    include_positions: bool = Query(False, description="Include employee positions")
):
    controller = EmployeeController(db, params)
    result = await controller.get_all_employees(filters=filters, include_positions=include_positions)
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
