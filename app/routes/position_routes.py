from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.base import SessionLocal
from app.services.position_service import PositionService
from app.dtos.position_dto import PositionCreateDTO, PositionUpdateDTO

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_positions(db: Session = Depends(get_db)):
    service = PositionService(db)
    return service.get_all_positions()

@router.get("/{position_id}")
def get_position(position_id: int, db: Session = Depends(get_db)):
    service = PositionService(db)
    position = service.get_position(position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position

@router.post("/")
def create_position(position: PositionCreateDTO, db: Session = Depends(get_db)):
    service = PositionService(db)
    return service.create_position(position)

@router.put("/{position_id}")
def update_position(position_id: int, position: PositionUpdateDTO, db: Session = Depends(get_db)):
    service = PositionService(db)
    updated_position = service.update_position(position_id, position)
    if not updated_position:
        raise HTTPException(status_code=404, detail="Position not found")
    return updated_position

@router.delete("/{position_id}")
def delete_position(position_id: int, db: Session = Depends(get_db)):
    service = PositionService(db)
    service.delete_position(position_id)
    return {"detail": "Position deleted"}
