from datetime import date
from typing import Optional
from pydantic import BaseModel

class PositionCreateDTO(BaseModel):
    descripcion: str
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    importe: float

class PositionUpdateDTO(BaseModel):
    descripcion: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    importe: Optional[float] = None
