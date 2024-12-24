from datetime import date
from pydantic import BaseModel

class Employee(BaseModel):
    id: int
    legajo: str
    nombre: str
    apellido: str
    documento: str
    fecha_ingreso: date
