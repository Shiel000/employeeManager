from datetime import date
from typing import Optional
from pydantic import BaseModel

class PositionDetailCreateDTO(BaseModel):
    salary: float
    start_date: date
    end_date: Optional[date] = None  # Esto hace que `end_date` sea opcional

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "salary": 20000.00,
                "start_date": "2024-10-24",
                "end_date": None
            }
        }

