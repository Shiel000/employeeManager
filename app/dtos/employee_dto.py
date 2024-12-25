from datetime import date
from pydantic import BaseModel

class EmployeeCreateDTO(BaseModel):
    record: str
    name: str
    surname: str
    document: int
    entry_date: date
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                    "record": "23456",
                    "name": "Jane",
                    "surname": "Doe",
                    "document": "39098765",
                    "entry_date": "2024-12-24",
            }
        }
    
    @property
    def full_name(self) -> str:
        """Combina nombre y apellido."""
        return f"{self.name} {self.surname}"

    @property
    def seniority(self) -> int:
        """Calcula la antigüedad del empleado en años."""
        today = date.today()
        return today.year - self.entry_date.year - (
            (today.month, today.day) < (self.entry_date.month, self.entry_date.day)
        )
    



class EmployeeUpdateDTO(BaseModel):
    name: str
    surname: str
    entry_date: date 