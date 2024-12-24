from datetime import date
from pydantic import BaseModel

class EmployeeCreateDTO(BaseModel):
    legajo: str
    nombre: str
    apellido: str
    documento: str
    fecha_ingreso: date

class EmployeeUpdateDTO(BaseModel):
    nombre: str
    apellido: str
    fecha_ingreso: date
