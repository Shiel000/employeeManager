from datetime import date
from pydantic import BaseModel,validator
from typing import Optional, List
from fastapi import Query
from app.dtos.position_dto import PositionOut

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
    
    # @property
    # def full_name(self) -> str:
    #     """Combina nombre y apellido."""
    #     return f"{self.name} {self.surname}"

    # @property
    # def seniority(self) -> int:
    #     """Calcula la antigüedad del empleado en años."""
    #     today = date.today()
    #     return today.year - self.entry_date.year - (
    #         (today.month, today.day) < (self.entry_date.month, self.entry_date.day)
    #     )
    

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



class EmployeeOut(BaseModel):
    id: int
    employee_number: int
    name: str
    surname: str
    document: int
    entry_date: date
    positions: Optional[List[dict]] = None


    class Config:
        from_attributes = True
        # json_encoders = {
        #     # Excluir campos None automáticamente
        #     Optional: lambda v: v if v is not None else None
        # }
