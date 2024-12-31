from datetime import date
from typing import Optional
from pydantic import BaseModel,Field
from app.dtos.position_detail_dto import PositionDetailCreateDTO

class PositionOutDTODTO(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True

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
    salary: float = Field(..., description="New salary for the position")
        
class PositionOutDTO(BaseModel):
    id: int
    description: str
    active: bool
    salary: Optional[float] = None 

    class Config:
        from_attributes = True
        
        
class PositionOutDTOWithDetailDTO(PositionOutDTO):
    start_date: Optional[date]
    end_date: Optional[date]
    salary: Optional[float]

    class Config:
        from_attributes = True

class PositionFilterDTO(BaseModel):
    start_date: Optional[date] = Field(None, description="Filter positions starting from this date")
    salary_min: Optional[float] = Field(None, description="Filter positions with a salary above this value")
    salary_max: Optional[float] = Field(None, description="Filter positions with a salary below this value")
    active: Optional[bool] = Field(None, description="Filter positions by active status")
