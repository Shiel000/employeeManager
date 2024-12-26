from datetime import date
from typing import Optional
from pydantic import BaseModel

class GroupCreateDTO(BaseModel):
    id : Optional[int] = None
    description : str
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                    "id": "1000",
                    "description": "Group 1",
            }
        }
    

class GroupUpdateDTO(BaseModel):
    description : str
