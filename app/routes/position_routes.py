from app.dtos.position_dto import PositionCreateDTO, PositionUpdateDTO,PositionOutDTO,PositionOutDTOWithDetailDTO,PositionFilterDTO
from app.controllers.position_controller import PositionController
from fastapi import APIRouter, Depends, HTTPException
from app.models.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page,Params


router = APIRouter()


@router.post("/", response_model=PositionOutDTO)
async def create_position(position: PositionCreateDTO, db: AsyncSession = Depends(get_db)):
    controller = PositionController(db)
    try:
        return await controller.create_position(position)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=Page[PositionOutDTOWithDetailDTO])
async def get_positions(
    filters: PositionFilterDTO = Depends(), 
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
