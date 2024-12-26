from sqlalchemy.orm import Session
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.position_repository import PositionRepository
from app.dtos.employee_dto import EmployeeCreateDTO, EmployeeUpdateDTO
from app.models.employee_model import EmployeeModel
from datetime import date
from typing import List, Optional
from app.models.position_model import PositionModel
from app.models.employee_position_table import EmployeePosition
from app.repositories.employee_position_repository import EmployeePositionRepository


class EmployeeService:
    def __init__(self, db: Session):
        self.repository = EmployeeRepository(db)
        self.position_repository = PositionRepository(db)
        self.employee_position_repository = EmployeePositionRepository(db)
        self.db = db
        
        
    def create_employee(self, employee_data: EmployeeCreateDTO):
        try:
            with self.db.begin():
                self._validate_document_uniqueness(employee_data.document)
                new_employee = self._create_new_employee(employee_data)
                positions = self._validate_and_get_positions(employee_data.positions)
                self._assign_positions_to_employee(new_employee, positions)
            self.db.refresh(new_employee)
            return self._build_employee_response(new_employee, positions)
        except Exception as e:
            print(f"Error while creating employee: {e}")
            raise e
        
    def _validate_document_uniqueness(self, document: int):
        existing_employee = self.repository.get_by_document(document)
        if existing_employee:
            raise ValueError("An employee with this document already exists.")
        
    def _create_new_employee(self, employee_data: EmployeeCreateDTO) -> EmployeeModel:
        employee_number = self.calculate_employee_number()
        new_employee = EmployeeModel(
            employee_number=employee_number,
            name=employee_data.name,
            surname=employee_data.surname,
            document=employee_data.document,
            entry_date=employee_data.entry_date
        )
        self.repository.create(new_employee)
        return new_employee
    
    def _validate_and_get_positions(self, position_ids: List[int]) -> List[PositionModel]:
        if not position_ids:
            raise ValueError("An employee must have at least one position assigned.")
        positions = self.position_repository.get_by_ids(position_ids, is_active=True)
        if not positions or len(positions) != len(position_ids):
            raise ValueError("Some positions provided are invalid.")
        if len(positions) > 3:
            raise ValueError("An employee cannot have more than 3 active positions.")
        return positions

    def _assign_positions_to_employee(self, employee: EmployeeModel, positions: List[PositionModel]):
        for position in positions:
            employee_position = EmployeePosition(
                employee=employee,
                position=position,
                start_date=date.today(),
                end_date=None
            )
            self.employee_position_repository.create(employee_position)
            # self.db.add(employee_position)
            
            
    def _build_employee_response(self, employee: EmployeeModel, positions: List[PositionModel]) -> dict:
        return {
            "id": employee.id,
            "employee_number": employee.employee_number,
            "name": employee.name,
            "surname": employee.surname,
            "document": employee.document,
            "entry_date": employee.entry_date,
            "positions": [position.id for position in positions]
        }
   

    def calculate_employee_number(self):
        last_employee = self.repository.get_last_employee()
        return last_employee.employee_number + 1 if last_employee else 1
    
    
    def update_employee(self, employee_id: int, update_data: EmployeeUpdateDTO):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        if update_data.name:
            employee.name = update_data.name
        if update_data.surname:
            employee.surname = update_data.surname

        self.db.commit()
        self.db.refresh(employee)
        return employee

    def add_positions_to_employee(self, employee_id: int, positions: List[int]):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        active_positions = self.position_repository.get_by_ids(positions, is_active=True)
        if len(active_positions) + len([ep for ep in employee.employee_positions if ep.end_date is None]) > 3:
            raise ValueError("An employee cannot have more than 3 active positions.")

        for position in active_positions:
            # Crear y guardar un nuevo registro en EmployeePosition
            employee_position = EmployeePosition(
                employee_id=employee.id,
                position_id=position.id,
                start_date=date.today(),
                end_date=None
            )
            self.employee_position_repository.create(employee_position)

        self.db.commit()
        self.db.refresh(employee)
        # self._build_employee_response(employee=employee,positions=active_positions)
        return employee

    
    def remove_positions_from_employee(self, employee_id: int, positions: List[int]):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        # Obtener las relaciones activas desde el repositorio
        relationships = self.employee_position_repository.get_active_relationships(employee_id, positions)
        if not relationships:
            raise ValueError("No active relationships found for the given positions.")

        # Actualizar la fecha de finalización
        self.employee_position_repository.update_relationship_end_date(relationships, date.today())

        self.db.commit()
        self.db.refresh(employee)
        return employee
    
    def get_position_history(self, employee_id: Optional[int] = None, employee_number: Optional[int] = None):
    
        if not employee_id and not employee_number:
            raise ValueError("Either employee_id or employee_number must be provided.")

        if employee_id:
            employee = self.repository.get_by_id(employee_id)
        elif employee_number:
            employee = self.repository.get_by_employee_number(employee_number)

        if not employee:
            raise ValueError("Employee not found.")

        # Construir el historial de posiciones
        return [
            {
                "position_id": ep.position_id,
                "start_date": ep.start_date,
                "end_date": ep.end_date,
            }
            for ep in employee.employee_positions
        ]


    
    def list_employees(self, name: Optional[str], surname: Optional[str], active_position: Optional[bool], skip: int, limit: int):
        """
        Lista empleados con filtros opcionales, paginación y ordenación.
        """
        filters = {}
        if name:
            filters["name"] = name
        if surname:
            filters["surname"] = surname
        if active_position is not None:
            filters["active_position"] = active_position

        employees = self.repository.list_employees(filters, skip, limit)
        return [
            {
                "id": emp.id,
                "employee_number": emp.employee_number,
                "name": emp.name,
                "surname": emp.surname,
                "positions": [
                    {
                        "position_id": ep.position_id,
                        "start_date": ep.start_date,
                        "end_date": ep.end_date,
                    }
                    for ep in emp.employee_positions
                    if not active_position or ep.end_date is None  # Filtro aplicado a la salida
                ]
            }
            for emp in employees
        ]
    
    def get_employee(self, employee_id: int):
        """
        Obtiene un empleado y sus posiciones activas e históricas.
        """
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        return {
            "id": employee.id,
            "employee_number": employee.employee_number,
            "name": employee.name,
            "surname": employee.surname,
            "document": employee.document,
            "entry_date": employee.entry_date,
            "positions": [
                {
                    "position_id": ep.position_id,
                    "start_date": ep.start_date,
                    "end_date": ep.end_date,
                    "is_active": ep.end_date is None
                }
                for ep in employee.employee_positions
            ]
        }
    
    def delete_employee(self, employee_id: int):
        """
        Elimina un empleado después de desvincularlo de sus cargos.
        """
        # Obtener el empleado
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        # Desvincular al empleado de sus cargos
        active_positions = self.employee_position_repository.get_active_relationships(employee_id, [])
        for position in active_positions:
            position.end_date = date.today()
        
        # Eliminar al empleado
        self.repository.delete(employee)

        # Guardar los cambios
        self.db.commit()
        return {"detail": f"Employee with ID {employee_id} has been deleted."}
    
        # def create_employee(self, employee_data: EmployeeCreateDTO):
    #     try:
    #         with self.db.begin():
 
    #             existing_employee = self.repository.get_by_document(employee_data.document)
    #             if existing_employee:
    #                 raise ValueError("An employee with this document already exists.")

    #             # Calcular el número del empleado
    #             employee_number = self.calculate_employee_number()

    #             # Crear el empleado
    #             new_employee = EmployeeModel(
    #                 employee_number=employee_number,
    #                 name=employee_data.name,
    #                 surname=employee_data.surname,
    #                 document=employee_data.document,
    #                 entry_date=employee_data.entry_date
    #             )
    #             # self.db.add(new_employee)
    #             self.repository.create(new_employee)

    #             if not employee_data.positions:
    #                 raise ValueError("An employee must have at least one position assigned.")

    #             positions = self.position_repository.get_by_ids(employee_data.positions, is_active=True)
    #             if not positions or len(positions) != len(employee_data.positions):
    #                 raise ValueError("Some positions provided are invalid.")

    #             if len(positions) > 3:
    #                 raise ValueError("An employee cannot have more than 3 active positions.")

    #             for position in positions:
    #                 employee_position = EmployeePosition(
    #                     employee=new_employee,
    #                     position=position,
    #                     start_date=date.today(),
    #                     end_date=None
    #                 )
    #                 self.db.add(employee_position)

    #         self.db.refresh(new_employee)

    #         return {
    #             "id": new_employee.id,
    #             "employee_number": new_employee.employee_number,
    #             "name": new_employee.name,
    #             "surname": new_employee.surname,
    #             "document": new_employee.document,
    #             "entry_date": new_employee.entry_date,
    #             "positions": [position.id for position in positions]
    #         }
    #     except Exception as e:
    #         print(f"Error while creating employee: {e}")
    #         raise e
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    # def get_all_employees(self):
    #     return self.repository.get_all()

    # def get_employee(self, employee_id: int):
    #     return self.repository.get_by_id(employee_id)

    # def create_employee(self, employee_data: EmployeeCreateDTO):
    #     employee = EmployeeModel(**employee_data.dict())
    #     return self.repository.create(employee)

    # # def update_employee(self, employee_id: int, employee_data: EmployeeUpdateDTO):
    # #     employee = self.repository.get_by_id(employee_id)
    # #     if not employee:
    # #         raise ValueError("Employee not found")
    # #     for key, value in employee_data.dict(exclude_unset=True).items():
    # #         setattr(employee, key, value)
    # #     return self.repository.update(employee)
    

    # def update_employee(self, employee_id: int, employee_data: EmployeeUpdateDTO):
    #     employee = self.repository.get_by_id(employee_id)
    #     if not employee:
    #         raise ValueError("Employee not found")

    #     # Actualizar solo los campos definidos
    #     for key, value in employee_data.dict(exclude_unset=True).items():
    #         setattr(employee, key, value)

    #     return self.repository.update(employee)


    # def delete_employee(self, employee_id: int):
    #     employee = self.repository.get_by_id(employee_id)
    #     if not employee:
    #         raise ValueError("Employee not found")
    #     self.repository.delete(employee)