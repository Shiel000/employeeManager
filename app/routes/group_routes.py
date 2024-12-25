from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.controllers.group_controller import GroupController
from app.dtos.group_dto import GroupCreateDTO, GroupUpdateDTO

router = APIRouter()

@router.get("/")
def get_groups(db: Session = Depends(get_db), include_positions: bool = True):
    controller = GroupController(db)
    return controller.get_all_groups(include_positions=include_positions)

@router.get("/{group_id}")
def get_group(group_id: int, db: Session = Depends(get_db)):
    controller = GroupController(db)
    try:
        return controller.get_group(group_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/")
def create_group(group: GroupCreateDTO, db: Session = Depends(get_db)):
    controller = GroupController(db)
    try:
        return controller.create_group(group)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{group_id}")
def update_group(group_id: int, group: GroupUpdateDTO, db: Session = Depends(get_db)):
    controller = GroupController(db)
    try:
        return controller.update_group(group_id, group)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    controller = GroupController(db)
    try:
        controller.delete_group(group_id)
        return {"detail": "group deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
