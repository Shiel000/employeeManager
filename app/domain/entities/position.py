from datetime import date
from pydantic import BaseModel

class Position(BaseModel):
    id: int
    descripcion: str
    fecha_inicio: date
    fecha_fin: date | None = None
    importe: float

    class Config:
        orm_mode = True
