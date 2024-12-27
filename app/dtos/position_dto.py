from datetime import date
from typing import Optional
from pydantic import BaseModel
from app.dtos.position_detail_dto import PositionDetailCreateDTO

class PositionCreateDTO(BaseModel):
    description: str
    detail: PositionDetailCreateDTO

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Manager",
                "detail": {
                    "salary": 20000.00,
                    "start_date": "2024-10-24",
                    "end_date": None,
                },
            }
        }


# # DTO para actualizar una posición (solo descripción)
class PositionUpdateDTO(BaseModel):
    id: int
    salary : float
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "1",
                "salary" : 50000
            }
        }
        
class PositionOut(BaseModel):
    id: int
    description: str
    active: bool

    class Config:
        from_attributes = True