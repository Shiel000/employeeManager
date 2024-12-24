from datetime import date
from pydantic import BaseModel

class EmployeeCreateDTO(BaseModel):
    legajo: str
    nombre: str
    apellido: str
    documento: str
    fecha_ingreso: date
    
    @property
    def full_name(self) -> str:
        """Combina nombre y apellido."""
        return f"{self.nombre} {self.apellido}"

    @property
    def seniority(self) -> int:
        """Calcula la antigüedad del empleado en años."""
        today = date.today()
        return today.year - self.fecha_ingreso.year - (
            (today.month, today.day) < (self.fecha_ingreso.month, self.fecha_ingreso.day)
        )
    
    class Config:
        json_schema_extra = {
            "example": {
                    "legajo": "23456",
                    "nombre": "Jane",
                    "apellido": "Doe",
                    "documento": "39098765",
                    "fecha_ingreso": "2024-12-24",
            }
        }


class EmployeeUpdateDTO(BaseModel):
    nombre: str
    apellido: str
    fecha_ingreso: date 
