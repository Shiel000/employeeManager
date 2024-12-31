from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee_model import EmployeeModel
from app.models.position_model import PositionModel
from app.models.payroll_model import PayrollModel
from app.models.position_detail_model import PositionDetailModel
from app.models.employee_position_table import EmployeePosition
from faker import Faker
from datetime import date, timedelta

fake = Faker()

async def create_positions(db: AsyncSession):
    positions = [
        PositionModel(description=fake.job(), active=True) for _ in range(10)
    ]
    db.add_all(positions)
    await db.commit()  # Asincrónico
    return positions


async def create_position_details(db: AsyncSession, positions):
    for position in positions:
        start_date = fake.date_between(start_date='-8y', end_date='-1y')
        detail = PositionDetailModel(
            position_id=position.id,
            salary=fake.random_int(min=3000, max=10000),
            start_date=start_date,
            end_date=None  # No end date
        )
        db.add(detail)
    await db.commit()
    print(f"Details created for {len(positions)} positions.")


async def create_employees(db: AsyncSession):
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
    await db.commit()
    return employees


async def create_employee_positions(db: AsyncSession, employees, positions):
    print('\n',"entre") 
    for employee in employees:
        assigned_positions = fake.random_elements(elements=positions, length=fake.random_int(min=1, max=3), unique=True)
        for position in assigned_positions:
            print('\n',"employee --> ",employee,'\n')
            print('\n',"position --> ",position,'\n')
            association = EmployeePosition(
                employee_id=employee.id,
                position_id=position.id,
                start_date=fake.date_between(start_date=employee.entry_date, end_date=date.today()),
                end_date=None  # No end date for active positions
            )
            print('\n',association,'\n')
            db.add(association)
    await db.commit()
    print("Employee-position associations created dynamically.")



async def populate_dummy_data(async_session_maker):
    async with async_session_maker() as db:
        positions = await create_positions(db)
        await create_position_details(db, positions)
        employees = await create_employees(db)

        print(f"Employees created: {len(employees)}")
        print(f"Positions created: {len(positions)}")

        await create_employee_positions(db, employees, positions)
        print("Dummy data populated successfully!")


# from sqlalchemy.orm import Session
# from app.models.employee_model import EmployeeModel
# from app.models.position_model import PositionModel
# from app.models.payroll_model import PayrollModel
# from app.models.position_detail_model import PositionDetailModel
# from app.models.employee_position_table import EmployeePosition
# from faker import Faker
# from datetime import date, timedelta
# import random
# from app.models.base import SessionLocal
# fake = Faker()




# def create_positions(db, fake):
#     positions = [
#         PositionModel(description=fake.job(), active=True) for _ in range(10)
#     ]
#     db.add_all(positions)
#     db.commit()
#     print(f"{len(positions)} positions created.")
#     return positions


# def create_position_details(db, fake, positions):
#     for position in positions:
#         start_date = fake.date_between(start_date='-8y', end_date='-1y')
#         detail = PositionDetailModel(
#             position_id=position.id,
#             salary=fake.random_int(min=3000, max=10000),
#             start_date=start_date,
#             # end_date=start_date + timedelta(days=365)  # Duration of 1 year
#             end_date=None
#         )
#         db.add(detail)
#     db.commit()
#     print(f"Details created for {len(positions)} positions.")


# def create_employees(db, fake):
#     employees = [
#         EmployeeModel(
#             name=fake.first_name(),
#             surname=fake.last_name(),
#             employee_number=fake.unique.random_int(min=1, max=1000),
#             document=fake.unique.random_int(min=1000000, max=99999999),
#             entry_date=fake.date_between(start_date='-4y', end_date='today')
#         )
#         for _ in range(10)
#     ]
#     db.add_all(employees)
#     db.commit()  # Confirmar transacción aquí
#     return db.query(EmployeeModel).all()





# def create_employee_positions(db, fake, employees, positions):
#     for employee in employees:
#         # Selecciona entre 1 y 3 posiciones únicas aleatorias
#         assigned_positions = fake.random_elements(elements=positions, length=fake.random_int(min=1, max=3), unique=True)
#         for position in assigned_positions:
#             association = EmployeePosition(
#                 employee_id=employee.id,
#                 position_id=position.id,
#                 start_date=fake.date_between(start_date=employee.entry_date, end_date=date.today()),
#                 end_date=None  # No end date for active positions
#             )
#             print('\n',association,'\n')
#             db.add(association)
    
#     db.commit()
#     print(f"Employee-position associations created dynamically.")
    
# def populate_dummy_data():
#     db = SessionLocal()
#     fake = Faker()
#     try:
#         positions = create_positions(db, fake)
#         create_position_details(db, fake, positions)
#         employees = create_employees(db, fake)
        
        
#         print(f"Employees created: {len(employees)}")
#         print(f"Positions created: {len(positions)}")
        
#         create_employee_positions(db, fake, employees, positions)
#         print("Dummy data populated successfully!")
#     finally:
#         db.close()
