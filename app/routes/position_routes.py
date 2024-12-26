from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.controllers.position_controller import PositionController
from app.dtos.position_dto import PositionCreateDTO, PositionUpdateDTO

router = APIRouter()


# Create
@router.post("/")
def create_position(position: PositionCreateDTO, db: Session = Depends(get_db)):
    controller = PositionController(db)
    try:
        return controller.create_position(position)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# List all (with or without details)
@router.get("/")
def get_positions(db: Session = Depends(get_db), include_details: bool = True):
    controller = PositionController(db)
    return controller.get_all_positions(include_details=include_details)

# List one
@router.get("/{position_id}")
def get_position(position_id: int, db: Session = Depends(get_db), include_detail: bool = True):
    controller = PositionController(db)
    try:
        return controller.get_position(position_id, include_detail=include_detail)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

#Edit detail
@router.put("/{position_id}/edit")
def edit_position(position_data: PositionUpdateDTO, db: Session = Depends(get_db)):
    controller = PositionController(db)
    try:
        return controller.edit_position(position_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Deactivate 
@router.delete("/{position_id}")
def deactivate_position(position_id: int, db: Session = Depends(get_db)):
    controller = PositionController(db)
    try:
        controller.deactivate_position(position_id)
        return {"detail": "Position deactivated"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# Activate
@router.put("/{position_id}/activate")
def update_position_status(position_id: int, db: Session = Depends(get_db)):
    controller = PositionController(db)
    try:
        return controller.activate_position(position_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))





# @router.get("/")
# def get_positions(db: Session = Depends(get_db), include_salary: bool = True):
#     controller = PositionController(db)
#     return controller.get_all_positions(include_salary=include_salary)
