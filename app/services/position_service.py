from app.repositories.position_repository import PositionRepository
from app.models.position_model import PositionModel
from app.models.position_detail_model import PositionDetailModel
from app.dtos.position_dto import PositionCreateDTO, PositionUpdateDTO, PositionOut,PositionOutWithDetailDTO,PositionFilterDTO
from app.repositories.position_detail_repository import PositionDetailRepository
from app.services.position_detail_service import PositionDetailService
from app.repositories.employee_position_repository import EmployeePositionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page,paginate
from typing import Optional
from datetime import date



class PositionService:
    def __init__(self, db: AsyncSession,params=None):
        self.position_repository = PositionRepository(db)
        self.detail_service = PositionDetailService(db)
        self.employee_position_repository = EmployeePositionRepository(db)
        self.detail_repository = PositionDetailRepository(db)
        self.db = db
        self.params =params

    async def create_position(self, position_data: PositionCreateDTO) -> PositionOut:
        # Validar si la posición ya existe
        existing_position = await self.position_repository.get_by_name(position_data.description)
        if existing_position:
            raise ValueError(f"A position with the name '{position_data.description}' already exists.")

        # Crear la posición
        position = PositionModel(description=position_data.description, active=True)
        await self.position_repository.create(position)

        # Crear el detalle asociado
        await self.detail_service.create_detail(position=position, detail_data=position_data.detail)

        # Confirmar cambios en la base de datos
        await self.db.commit()
        await self.db.refresh(position)

        # Convertir a esquema Pydantic antes de devolverlo
        return PositionOut.from_orm(position)
    
    
    async def get_all_positions(self, filters: PositionFilterDTO) -> Page[PositionOutWithDetailDTO]:
        positions = await self.position_repository.get_all(filters)

        # Mapear posiciones con detalles
        positions_with_details = []
        for position in positions:
            active_detail = await self.detail_service.get_active_detail(position.id)
            positions_with_details.append(PositionOutWithDetailDTO(
                id=position.id,
                description=position.description,
                active=position.active,
                start_date=active_detail.start_date if active_detail else None,
                end_date=active_detail.end_date if active_detail else None,
                salary=active_detail.salary if active_detail else None,
            ))

        return paginate(positions_with_details, self.params)

    async def get_position(self, position_id: int) -> Optional[dict]:
        # Obtener posición por ID
        position = await self.position_repository.get_by_id(position_id)
        if not position:
            raise ValueError("Position not found")
        detail = await self.detail_service.get_active_detail(position_id)
        return {
            "description": position.description,
            "active": position.active,
            "start_date": detail.start_date if detail else None,
            "end_date": detail.end_date if detail else None,
            "salary": detail.salary if detail else None,
        }
        
        
    async def edit_position(self, position_id: int, position_data: PositionUpdateDTO):
        # Validar posición
        position = await self.position_repository.get_by_id(position_id)
        if not position or not position.active:
            raise ValueError("Position not found or inactive")

        # Actualizar el detalle activo
        new_detail = await self.detail_service.update_active_detail(
            position=position, new_salary=position_data.salary
        )

        # Confirmar cambios y refrescar datos
        await self.db.commit()
        await self.db.refresh(position)
        await self.db.refresh(new_detail) 
        
        response = PositionOut.from_orm(position)
        response.salary = new_detail.salary
        return response

    async def update_active_status(self, position_id: int, is_active: bool) -> PositionModel:
        # Obtener la posición por ID
        position = await self.position_repository.get_by_id(position_id)
        if not position:
            raise ValueError("Position not found")
        
        # Actualizar el estado activo
        position.active = is_active
        await self.db.commit()
        await self.db.refresh(position)
        return position

    async def delete_position(self, position_id: int) -> None:
        # Validar si la posición existe
        position = await self.position_repository.get_by_id(position_id)
        if not position:
            raise ValueError("Position not found.")
        
        # Validar que no esté activa
        if position.active:
            raise ValueError("Cannot delete an active position.")

        # Validar que no esté relacionada con empleados
        related_employees = await self.employee_position_repository.get_related_employees(position_id)
        if related_employees:
            raise ValueError("Cannot delete position because it is linked to employees.")

        # Eliminar detalles asociados
        await self.detail_repository.delete_by_position_id(position_id)

        # Eliminar posición
        await self.position_repository.delete(position)

        # Confirmar cambios
        await self.db.commit()

    
    
# class PositionService:
#     def __init__(self, db: Session):
#         self.position_repository = PositionRepository(db)
#         self.detail_repository = PositionDetailRepository(db)
#         self.detail_service = PositionDetailService(db)
#         self.employee_position_repository = EmployeePositionRepository(db)
#         self.db = db
        
    
#     def create_position(self, position_data: PositionCreateDTO):    
#         existing_position = self.position_repository.get_by_name(position_data.description)
#         if existing_position:
#             raise ValueError(f"A position with the name '{position_data.description}' already exists.")

#         position = PositionModel(description=position_data.description, active=True)
#         self.position_repository.create(position)
#         self.detail_service.create_detail(position=position, detail_data=position_data.detail)
#         self.db.commit()
#         self.db.refresh(position)
#         return position

      
#     def update_active_status(self, position_id: int, is_active: bool):
#         position = self.position_repository.get_by_id(position_id)
#         if not position:
#             raise ValueError("Position not found")
#         position.active = is_active
#         self.db.commit()
#         self.db.refresh(position)
#         return position

#     def edit_position(self, position_data: PositionUpdateDTO):
        
#         position_id = position_data.id
#         salary = position_data.salary  
#         position = self.position_repository.get_by_id(position_id)
#         if not position or not position.active:
#             raise ValueError("Position not found or inactive")

#         new_detail = self.detail_service.update_active_detail(position=position, new_salary=salary)

#         self.db.commit()
#         self.db.refresh(position)
#         return {
#                 "id": position.id,
#                 "description": position.description,
#                 "active": position.active,
#                 "updated_salary": new_detail.salary
#             }
            
#     def get_all_positions(self):
#         return self.position_repository.get_all()

#     def get_position(self, position_id: int):
#         position = self.position_repository.get_by_id(position_id)
#         if not position:
#             raise ValueError("Position not found")
#         return position

#     def get_all_positions_with_details(self):
#         positions = self.position_repository.get_all()
#         result = []

#         for position in positions:
#             active_detail = self.detail_service.get_active_detail(position.id)
#             result.append({
#                 "description": position.description,
#                 "active": position.active,
#                 "start_date": active_detail.start_date if active_detail else None,
#                 "end_date": active_detail.end_date if active_detail else None,
#                 "salary": active_detail.salary if active_detail else None,
#             })

#         return result
    
#     def delete_position(self, position_id: int):
    
#         position = self.position_repository.get_by_id(position_id)
#         if not position:
#             raise ValueError("Position not found.")
#         if position.active:
#             raise ValueError("Cannot delete an active position.")
#         related_employees = self.employee_position_repository.get_related_employees(position_id)
#         if related_employees:
#             raise ValueError("Cannot delete position because it is linked to employees.")


#         self.detail_repository.delete_by_position_id(position_id)
#         self.position_repository.delete(position)
#         self.db.commit()

