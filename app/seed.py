from sqlalchemy.orm import Session
from app.models.employee_model import EmployeeModel
from app.models.position_model import PositionModel
from app.models.payroll_model import PayrollModel
from app.models.position_detail_model import PositionDetailModel
from app.models.employee_position_table import EmployeePosition
from faker import Faker
from datetime import date, timedelta
import random
from app.models.base import SessionLocal
fake = Faker()




def create_positions(db, fake):
    positions = [
        PositionModel(description=fake.job(), active=True) for _ in range(10)
    ]
    db.add_all(positions)
    db.commit()
    print(f"{len(positions)} positions created.")
    return positions


def create_position_details(db, fake, positions):
    for position in positions:
        start_date = fake.date_between(start_date='-8y', end_date='-1y')
        detail = PositionDetailModel(
            position_id=position.id,
            salary=fake.random_int(min=3000, max=10000),
            start_date=start_date,
            # end_date=start_date + timedelta(days=365)  # Duration of 1 year
            end_date=None
        )
        db.add(detail)
    db.commit()
    print(f"Details created for {len(positions)} positions.")


def create_employees(db, fake):
    employees = [
        EmployeeModel(
            name=fake.first_name(),
            surname=fake.last_name(),
            employee_number=fake.unique.random_int(min=1, max=1000),
            document=fake.unique.random_int(min=1000000, max=99999999),
            entry_date=fake.date_between(start_date='-4y', end_date='today')
        )
        for _ in range(10)
    ]
    db.add_all(employees)
    db.commit()  # Confirmar transacción aquí
    return db.query(EmployeeModel).all()





def create_employee_positions(db, fake, employees, positions):
    for employee in employees:
        # Selecciona entre 1 y 3 posiciones únicas aleatorias
        assigned_positions = fake.random_elements(elements=positions, length=fake.random_int(min=1, max=3), unique=True)
        for position in assigned_positions:
            association = EmployeePosition(
                employee_id=employee.id,
                position_id=position.id,
                start_date=fake.date_between(start_date=employee.entry_date, end_date=date.today()),
                end_date=None  # No end date for active positions
            )
            print('\n',association,'\n')
            db.add(association)
    
    db.commit()
    print(f"Employee-position associations created dynamically.")
    
def populate_dummy_data():
    db = SessionLocal()
    fake = Faker()
    try:
        positions = create_positions(db, fake)
        create_position_details(db, fake, positions)
        employees = create_employees(db, fake)
        
        
        print(f"Employees created: {len(employees)}")
        print(f"Positions created: {len(positions)}")
        
        create_employee_positions(db, fake, employees, positions)
        print("Dummy data populated successfully!")
    finally:
        db.close()

# def populate_dummy_data():
#     db = SessionLocal()
#     try:
#         # Aquí va tu lógica para poblar la base de datos
#         fake = Faker()
        
#         # Crea posiciones
#         positions = [
#             PositionModel(description=fake.job(), active=True) for _ in range(5)
#         ]
#         db.add_all(positions)
#         db.commit()

#         # Crea empleados
#         employees = [
#             EmployeeModel(
#                 name=fake.first_name(),
#                 surname=fake.last_name(),
#                 employee_number=fake.unique.random_int(min=1, max=1000),
#                 document=fake.unique.random_int(min=1000000, max=99999999),
#                 entry_date=fake.date_between(start_date='-10y', end_date='today')
#             )
#             for _ in range(10)
#         ]
#         db.add_all(employees)
#         db.commit()

#     finally:
#         db.close()
#     print("Dummy data populated successfully!")

# def populate_dummy_data():
#     db = SessionLocal()
#     try:
#         fake = Faker()
        
#         # Crear posiciones
#         positions = [
#             PositionModel(description=fake.job(), active=True) for _ in range(5)
#         ]
#         db.add_all(positions)
#         db.commit()
        
#         # Crear detalles de posición
#         for position in positions:
#             start_date = fake.date_between(start_date='-5y', end_date='-1y')
#             detail = PositionDetailModel(
#                 position_id=position.id,
#                 salary=fake.random_int(min=3000, max=10000),
#                 start_date=start_date,
#                 end_date=start_date + timedelta(days=365)  # Duración de un año
#             )
#             db.add(detail)
#         db.commit()

#         # Crear empleados
#         employees = [
#             EmployeeModel(
#                 name=fake.first_name(),
#                 surname=fake.last_name(),
#                 employee_number=fake.unique.random_int(min=1, max=1000),
#                 document=fake.unique.random_int(min=1000000, max=99999999),
#                 entry_date=fake.date_between(start_date='-10y', end_date='today')
#             )
#             for _ in range(10)
#         ]
#         db.add_all(employees)
#         db.commit()
        
#         # Asociar empleados con posiciones (EmployeePosition)
#         for employee in employees:
#             for position in fake.random_elements(elements=positions, length=2, unique=True):
#                 association = EmployeePosition(
#                     employee_id=employee.id,
#                     position_id=position.id,
#                     start_date=fake.date_between(start_date=employee.entry_date, end_date=date.today()),
#                     end_date=None  # Sin fecha de fin para posiciones activas
#                 )
#                 db.add(association)
#         db.commit()
        
#         print("Dummy data populated successfully!")
    
#     finally:
#         db.close()