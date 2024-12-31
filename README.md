# Employee Manager

## 🚀 1. Introduction

### 🔍 Overview  
This project is a robust system designed to manage **employees**, **job positions**, and **payroll processes** efficiently. It serves as a scalable and extensible backend for automating payroll calculations, tracking job assignments, and maintaining historical records.

---

### 🎯 Key Functionalities

#### 👩‍💼 Employee Management
- **Add, edit, and deactivate employees** in the system.
- Manage unique attributes for employees, such as:
  - Employee number.
  - Document ID.
- **Role assignment and tracking:**
  - Ensure at least **one active role** per employee.
  - Limit employees to **no more than three active roles** simultaneously.
- View detailed **role history**, including start and end dates.

#### 🏢 Position Management
- **Create, update, and deactivate job positions**.
- Associate **salary details** with positions while maintaining historical changes.
- Automatically **remove salary details** when a position is deleted.
- Prevent deletion of positions that are actively linked to employees.

#### 💵 Payroll Management
- **Calculate payroll** for individual employees or **batch process** for all employees.
- Components of payroll:
  - **Fixed minimum wage**.
  - Salaries from active positions.
  - **Seniority bonus** based on years of service.
- Prevent duplicate payroll entries for the same period.
- Export payroll data to **CSV** for reporting and backups.

#### 📊 Reporting and Analytics
- Generate comprehensive **payroll reports**, including:
  - Aggregation by **positions**.
  - Total and average amounts paid per position.
- Apply filters:
  - Date range.
  - Specific employees or positions.
- Export reports in **CSV format**.

#### 🛠️ Backup and Data Management
- Create **backups** of payroll data for specified periods.
- Restore or update payroll data from **CSV files**.
- **Clean up old payroll data** based on date ranges.

#### 📦 Seed Data for Testing
- Populate the database with **realistic dummy data** using `Faker`.
- Seed data includes:
  - Employees.
  - Positions.
  - Salary details.
  - Job assignments.

---

### 💻 Technology Stack
- **Backend Framework:** FastAPI (Python) 🐍
- **ORM:** SQLAlchemy for database management with **PostgreSQL** 🗄️
- **Environment:** Docker for containerized deployment 🐋
- **Libraries:**  
  - `Faker` for generating dummy data.
  - `fastapi-pagination` for paginated endpoints.
  - `pandas` for handling CSV exports and imports.
- **Testing and Development Tools:**  
  - Docker Compose for environment setup.
  - Custom seed scripts for populating the database.

---

This project is designed with **scalability**, **performance**, and **ease of use** in mind, making it an ideal solution for businesses managing payroll and employee data.

## 🛠️ 2. Installation

### ✅ Prerequisites
Before running the project, ensure the following are installed on your system:
- **Python 3.9** or later.
- **PostgreSQL** (Ensure a running instance with access credentials).
- **Docker** and **Docker Compose** (optional for containerized environments).

### ⚙️ Setting Up the Project
1. Clone the repository to your local machine:
```bash
     git clone https://github.com/Shiel000/employeeManager.git
     cd <repository-folder>
```
2. Build the Docker image:
```bash
    docker-compose build
```

3. Environment Variables:

    The project already includes required environment variables (DATABASE_URL, MINIMUM_WAGE, etc.) in the **docker-compose.yml file**.
    No additional configuration is necessary unless modifications are required.


4. Seed the database (optional):

    Uncomment the line **# populate_dummy_data()** in main.py under the startup event.
    Save the file and proceed with the next steps to populate the database.

## 🚀 3. Running the Project
### ▶️ Start the Project

- Run the Docker container:

    docker-compose up

    Access the API documentation via:
        Swagger: http://localhost:8001/docs
        Redoc: http://localhost:8001/redoc

### ℹ️ Notes:
- **Database Initialization**: If you've uncommented populate_dummy_data():
        Run the docker-compose up command to populate the database.
        After seeding, comment the line back in main.py to prevent duplicate data.
        Restart the container using:

        docker-compose down
        docker-compose up --build

With this setup, the project is fully configured to run in a Dockerized environment, with no need to manually manage dependencies or variables outside Docker Compose.


## 📖 API Routes

Below is a detailed breakdown of the main API routes, grouped by entity:

### 🧑‍💼 Employees
- **Create Employee**  
  **POST** `/api/employees/`  
  Request body:
  ```json
  {
      "name": "John",
      "surname": "Doe",
      "employee_number": 123,
      "document": 12345678,
      "entry_date": "2024-01-01"
  }

  Response:
  
    {
        "id": 1,
        "name": "John",
        "surname": "Doe",
        "employee_number": 123,
        "document": 12345678,
        "entry_date": "2024-01-01"
    }
    
- **List Employees**

  **GET** `/api/employees/` Supports filtering by name, surname, and position, along with pagination.

- **Edit Employee**

  **PUT** `/api/employees/{employee_id}`
    Request body:
  ```json
    {
        "name": "Jane",
        "surname": "Doe"
    }

- **Delete Employee**

  **DELETE** `/api/employees/{employee_id}`

### 🏷️ Positions

- **Create Position**
  
  **POST** `/api/positions/`
    ```json
    Request body:

    {
        "description": "Manager",
        "active": true
    }

- **List Positions**
    **GET** `/api/positions/`
    Supports filtering and includes optional details.

- **Activate/Deactivate Position**
   
   **PUT** `/api/positions/{position_id}/activate`

   **DELETE** `/api/positions/{position_id}`

- **Delete Position**
  
  **DELETE** `/api/positions/{position_id}`

### 💰 Payrolls

    Create Payroll for an Employee
    POST /api/payrolls/
    Request body:

{
    "employee_id": 1,
    "period": "2024-12"
}

Batch Payroll Creation
POST /api/payrolls/batch/
Request body:

{
    "period": "2024-12"
}

Generate Reports
GET /api/payrolls/operations/reports
Supports filtering by:

    Period (start and end date).
    Employee or Position.

Example response:

[
    {
        "position_description": "Manager",
        "total_liquidated": 5000.00,
        "average_per_employee": 1250.00
    },
    {
        "position_description": "Engineer",
        "total_liquidated": 4000.00,
        "average_per_employee": 1333.33
    }
]

Generate Backups in CSV
GET /api/payrolls/operations/backup
Supports filtering by:

    Period (start and end date).
    Employee ID.

Load Data from CSV
POST /api/payrolls/operations/upload-csv
Uploads and processes payroll data from a CSV file.

Delete Payrolls by Date Range
DELETE /api/payrolls/operations/
Request body:

    {
        "start_date": "2024-01",
        "end_date": "2024-12"
    }

📋 Example Requests and Responses

For detailed examples of request payloads and responses, refer to the API documentation automatically generated by FastAPI:
Swagger UI
ReDoc