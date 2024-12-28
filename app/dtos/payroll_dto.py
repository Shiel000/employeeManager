from pydantic import BaseModel, Field
from typing import Annotated,List,Optional
from datetime import date



class PayrollCreateDTO(BaseModel):
    employee_id: Annotated[int, Field(gt=0, description="The ID of the employee")]
    period: Annotated[str, Field(pattern=r"^\d{4}-\d{2}$", description="The payroll period in format YYYY-MM")]

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 1,
                "period": "2024-12"
            }
        }
        
        
class PayrollFilterDTO(BaseModel):
    employee_id: Optional[int] = Field(None, description="Filter by employee ID")
    start_date: Optional[date] = Field(None, description="Start date for payroll period")
    end_date: Optional[date] = Field(None, description="End date for payroll period")
    position_id : Optional[int] = Field(None, description="Filter by Position ID")

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 123,
                "start_date": "2024-12-01",
                "end_date": "2024-12-31",
                "position_id":1,
            }
        }


class PayrollOutDTO(BaseModel):
    id: int
    employee_id: int
    period: str
    amount: float
    employee_name: str
    employee_surname: str
    positions: List[dict]  # Lista de posiciones, cada una con ID y descripción

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "employee_id": 7,
                "period": "2024-12",
                "amount": 371400,
                "employee_name": "Martin",
                "employee_surname": "Jones",
                "positions": [
                    {"position_id": 1, "position_description": "Manager"},
                    {"position_id": 2, "position_description": "Engineer"},
                    {"position_id": 3, "position_description": "Sub director"},
                    {"position_id": 5, "position_description": "Colaborator"}
                ]
            }
        }

class PayrollBackupFilterDTO(BaseModel):
    start_date: Optional[date] = Field(None,description="Start date for payroll period (YYYY-MM-DD)")
    end_date: Optional[date] = Field(None, description="End date for payroll period (YYYY-MM-DD)")
    employee_id: Optional[int] = Field(None, description="Filter by employee ID")

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 123,
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
            }
        }
        
        
class PayrollReporteFilterDTO(BaseModel):
    start_date: Optional[date] = Field(None,description="Start date for payroll period (YYYY-MM-DD)")
    end_date: Optional[date] = Field(None, description="End date for payroll period (YYYY-MM-DD)")
    employee_id: Optional[int] = Field(None, description="Filter by employee ID")
    position_id: Optional[int] = Field(None, description="Filter by position ID")  # Asegúrate de que esto está presente

    class Config:
        json_schema_extra = {
            "example": {
                "employee_id": 123,
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "position_id": 5,
            }
        }
        

class PayrollDeleteFilterDTO(BaseModel):
    start_date: date = Field(..., description="Start date for deletion (YYYY-MM-DD)")
    end_date: date = Field(..., description="End date for deletion (YYYY-MM-DD)")
    employee_id: Optional[int] = Field(None, description="Filter by employee ID")

    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "employee_id": 123
            }
        }
                

class PayrollUploadDTO(BaseModel):
    overwrite_existing: bool = Field(
        default=False,
        description="Overwrite existing payroll records if they exist"
    )
    
    
    
# class PayrollBackupFilterDTO(BaseModel):
#     start_date: Optional[date] = Field(None,description="Start date for payroll period (YYYY-MM-DD)")
#     end_date: Optional[date] = Field(None, description="End date for payroll period (YYYY-MM-DD)")
#     employee_id: Optional[int] = Field(None, description="Filter by employee ID")

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "start_date": "2024-10-10",
#                 "end_date": "2025-10-10",
#                 "employee_id": 12
#             }
#         }
        