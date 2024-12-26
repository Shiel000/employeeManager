from sqlalchemy.orm import Session
from app.models.employee_position_table import EmployeePosition
from typing import  List
from datetime import date

class EmployeePositionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_active_relationships(self, employee_id: int, position_ids: List[int]):
        """
        Obtiene las relaciones activas entre un empleado y una lista de posiciones.
        """
        return (
            self.db.query(EmployeePosition)
            .filter(
                EmployeePosition.employee_id == employee_id,
                EmployeePosition.position_id.in_(position_ids),
                EmployeePosition.end_date == None
            )
            .all()
        )

    def update_relationship_end_date(self, relationships: List[EmployeePosition], end_date: date):
        for relationship in relationships:
            relationship.end_date = end_date
            
    def create(self, employee: EmployeePosition):
        self.db.add(employee)
        return employee

