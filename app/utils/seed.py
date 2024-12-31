from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee_model import EmployeeModel
from app.models.position_model import PositionModel
from app.models.payroll_model import PayrollModel
from app.models.position_detail_model import PositionDetailModel
from app.models.employee_position_table import EmployeePosition
from faker import Faker
from datetime import date

fake = Faker()

async def create_positions(db: AsyncSession):
    positions = [
        PositionModel(description=fake.job(), active=True) for _ in range(10)
    ]
    db.add_all(positions)
    await db.commit()
    for position in positions:
        await db.refresh(position)
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
    for employee in employees:
        await db.refresh(employee)
    return employees


async def create_employee_positions(db: AsyncSession, employees, positions):
    for employee in employees:
        await db.refresh(employee)
        assigned_positions = fake.random_elements(elements=positions, length=fake.random_int(min=1, max=3), unique=True)
        for position in assigned_positions:
            association = EmployeePosition(
                employee_id=employee.id,
                position_id=position.id,
                start_date=fake.date_between(start_date=employee.entry_date, end_date=date.today()),
                end_date=None
            )
            db.add(association)
    await db.commit()
    await db.refresh(association)
    print("Employee-position associations created dynamically.")



async def populate_dummy_data(db: AsyncSession):
    positions = await create_positions(db)
    await create_position_details(db, positions)
    employees = await create_employees(db)

    print(f"Employees created: {len(employees)}")
    print(f"Positions created: {len(positions)}")

    await create_employee_positions(db, employees, positions)
    print("Dummy data populated successfully!")
