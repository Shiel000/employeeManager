from datetime import date
from typing import Optional
from pydantic import BaseModel

class PositionCreateDTO(BaseModel):
    start_date : date
    end_date : Optional[date] = None
    general_id: int
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                    "start_date": "Jane",
                    "surname": "Doe",
                    "end_date": "39098765",
                    "general_id": "2024-12-24",
            }
        }
    

class PositionUpdateDTO(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[date] = None
    general_id: Optional[date] = None
