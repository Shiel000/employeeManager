from datetime import date
from pydantic import BaseModel,validator
from typing import Optional, List
from fastapi import Query


class EmployeeCreateDTO(BaseModel):
    name: str
    surname: str
    document: int
    entry_date: date
    positions: List[int]
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                    "name": "Jane",
                    "surname": "Doe",
                    "document": "39098765",
                    "entry_date": "2024-12-24",
                    "positions": [1,2]
            }
        }
    
class EmployeeUpdateDTO(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None

class EmployeeAddDeletePositionsDTO(BaseModel):
    positions: List[int]
    


class EmployeeFilter(BaseModel):
    name: Optional[str] = Query(None, description="Filter employees by name")
    surname: Optional[str] = Query(None, description="Filter employees by surname")
    position : Optional[int]= Query(None, description="Filter employees by positions")

    @validator("name", "surname")
    def validate_name_and_surname(cls, value):
        if value and len(value) < 2:
            raise ValueError("El nombre y el apellido deben tener al menos 2 caracteres.")
        return value



class EmployeeOutDRO(BaseModel):
    id: int
    employee_number: int
    name: str
    surname: str
    document: int
    entry_date: date
    positions: Optional[List[dict]] = None


    class Config:
        from_attributes = True
