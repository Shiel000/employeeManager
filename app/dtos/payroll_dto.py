from pydantic import BaseModel, Field
from typing import Annotated




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
        