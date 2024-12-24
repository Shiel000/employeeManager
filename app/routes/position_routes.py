from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.controllers.position_controller import PositionController
from app.dtos.position_dto import PositionCreateDTO, PositionUpdateDTO

router = APIRouter()

@router.get("/")
def get_positions(db: Session = Depends(get_db), include_salaries: bool = True):
    controller = PositionController(db)
    return controller.get_all_positions(include_salaries=include_salaries)

@router.get("/{position_id}")
def get_position(position_id: int, db: Session = Depends(get_db)):
    controller = PositionController(db)
    try:
        return controller.get_position(position_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
def create_position(position: PositionCreateDTO, db: Session = Depends(get_db)):
    controller = PositionController(db)
    try:
        return controller.create_position(position)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{position_id}")
def update_position(position_id: int, position: PositionUpdateDTO, db: Session = Depends(get_db)):
    controller = PositionController(db)
    try:
        return controller.update_position(position_id, position)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{position_id}")
def delete_position(position_id: int, db: Session = Depends(get_db)):
    controller = PositionController(db)
    try:
        controller.delete_position(position_id)
        return {"detail": "Position deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
