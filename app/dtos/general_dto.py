from datetime import date
from pydantic import BaseModel
from typing import Optional

class GeneralCreateDTO(BaseModel):
    id: int
    description : str
    aux_string1 : Optional[str] =None
    aux_string2 : Optional[str] =None
    aux_int1 : Optional[int] =None
    aux_int2 : Optional[int] =None
    aux_date1 : Optional[date] =None
    aux_date2 : Optional[date] =None
    group_id : int
    depends_on_id : Optional[int] =None
    
    class Config:
        json_schema_extra = {
            "example": {
                    "description": "General 1",
                    "aux_string1": "something",
                    "aux_string2": "",
                    "aux_int1": "",
                    "aux_int2": "",
                    "aux_date1": "",
                    "aux_date2": "",
                    "group_id": "1000",
                    "depends_on_id": ""
            }
        }


class GeneralUpdateDTO(BaseModel):
    description : str
    aux_string1 : Optional[str] =None
    aux_string2 : Optional[str] =None
    aux_int1 : Optional[int] =None
    aux_int2 : Optional[int] =None
    aux_date1 : Optional[date] =None
    aux_date2 : Optional[date] =None
    depends_on_id : Optional[int] =None