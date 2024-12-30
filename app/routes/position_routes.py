from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.controllers.position_controller import PositionController
from app.dtos.position_dto import PositionCreateDTO, PositionUpdateDTO,PositionOut,PositionOutWithDetailDTO,PositionFilterDTO
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page,Params


router = APIRouter()


@router.post("/", response_model=PositionOut)
async def create_position(position: PositionCreateDTO, db: AsyncSession = Depends(get_db)):
    controller = PositionController(db)
    try:
        return await controller.create_position(position)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=Page[PositionOutWithDetailDTO])
async def get_positions(
    filters: PositionFilterDTO = Depends(),  # Usar PositionFilter para estandarizar filtros
    db: AsyncSession = Depends(get_db),
    params: Params = Depends()
):
    controller = PositionController(db, params)
    return await controller.get_all_positions(filters=filters)

@router.get("/{position_id}")
async def get_position(
    position_id: int,
    db: AsyncSession = Depends(get_db)
):
    controller = PositionController(db)
    try:
        return await controller.get_position(position_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    

@router.put("/{position_id}/edit")
async def edit_position(
    position_id: int,
    position_data: PositionUpdateDTO,
    db: AsyncSession = Depends(get_db)
):
    controller = PositionController(db)
    try:
        return await controller.edit_position(position_id, position_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{position_id}/deactivate")
async def deactivate_position(position_id: int, db: AsyncSession = Depends(get_db)):
    controller = PositionController(db)
    try:
        await controller.deactivate_position(position_id)
        return {"detail": "Position deactivated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.put("/{position_id}/activate")
async def activate_position(position_id: int, db: AsyncSession = Depends(get_db)):
    controller = PositionController(db)
    try:
        await controller.activate_position(position_id)
        return {"detail": "Position activated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{position_id}")
async def delete_position(position_id: int, db: AsyncSession = Depends(get_db)):
    controller = PositionController(db)
    try:
        await controller.delete_position(position_id)
        return {"detail": "Position deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# # Create
# @router.post("/")
# def create_position(position: PositionCreateDTO, db: Session = Depends(get_db)):
#     controller = PositionController(db)
#     try:
#         return controller.create_position(position)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # List all (with or without details)
# @router.get("/")
# def get_positions(db: Session = Depends(get_db), include_details: bool = True):
#     controller = PositionController(db)
#     return controller.get_all_positions(include_details=include_details)

# # List one
# @router.get("/{position_id}")
# def get_position(position_id: int, db: Session = Depends(get_db), include_detail: bool = True):
#     controller = PositionController(db)
#     try:
#         return controller.get_position(position_id, include_detail=include_detail)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
    

# #Edit detail
# @router.put("/{position_id}/edit")
# def edit_position(position_data: PositionUpdateDTO, db: Session = Depends(get_db)):
#     controller = PositionController(db)
#     try:
#         return controller.edit_position(position_data)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # Deactivate 
# @router.delete("/{position_id}")
# def deactivate_position(position_id: int, db: Session = Depends(get_db)):
#     controller = PositionController(db)
#     try:
#         controller.deactivate_position(position_id)
#         return {"detail": "Position deactivated"}
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))
    
# # Activate
# @router.put("/{position_id}/activate")
# def update_position_status(position_id: int, db: Session = Depends(get_db)):
#     controller = PositionController(db)
#     try:
#         return controller.activate_position(position_id)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))


# @router.delete("/{position_id}/hard-delete")
# def delete_position(position_id: int, db: Session = Depends(get_db)):
#     controller = PositionController(db)
#     try:
#         return controller.delete_position(position_id)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))


# @router.get("/")
# def get_positions(db: Session = Depends(get_db), include_salary: bool = True):
#     controller = PositionController(db)
#     return controller.get_all_positions(include_salary=include_salary)
