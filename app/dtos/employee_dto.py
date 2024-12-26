from datetime import date
from pydantic import BaseModel
from typing import Optional, List

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
