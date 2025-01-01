# Employee Manager API

## 🚀 1. Introduction

### 🔍 Overview
This project is a robust system designed to manage employees, job positions, and payroll processes efficiently. It serves as a scalable and extensible backend for automating payroll calculations, tracking job assignments, and maintaining historical records.

---

## 🎯 2. Key Functionalities

### 👩‍💼 Employee Management
- Add, edit, and deactivate employees in the system.
- Manage unique attributes for employees, such as:
  - Employee number.
  - Document ID.
- Role assignment and tracking:
  - Ensure at least one active role per employee.
  - Limit employees to no more than three active roles simultaneously.
- View detailed role history, including start and end dates.

### 🏢 Position Management
- Create, update, and deactivate job positions.
- Associate salary details with positions while maintaining historical changes.
- Automatically remove salary details when a position is deleted.
- Prevent deletion of positions that are actively linked to employees.

### 💵 Payroll Management
- Calculate payroll for individual employees or batch process for all employees.
- Components of payroll:
  - Fixed minimum wage.
  - Salaries from active positions.
  - Seniority bonus based on years of service.
- Prevent duplicate payroll entries for the same period.
- Export payroll data to CSV for reporting and backups.

### 📊 Reporting and Analytics
- Generate comprehensive payroll reports, including:
  - Aggregation by positions.
  - Total and average amounts paid per position.
  - Total number of employees per position.
  - Percentage of total payroll per position.
- Apply filters:
  - Date range.
  - Specific employees or positions.
- Export reports in CSV format.


### 🛠️ Backup and Data Management
- Create backups of payroll data for specified periods.
- Restore or update payroll data from CSV files.
- Clean up old payroll data based on date ranges.

### 📦 Seed Data for Testing
- Populate the database with realistic dummy data using Faker.
- Seed data includes:
  - Employees.
  - Positions.
  - Salary details.
  - Job assignments.

---

## 💻 3. Technology Stack
- **Backend Framework**: FastAPI (Python) 🐍
- **ORM**: SQLAlchemy for database management with PostgreSQL 🗄️
- **Environment**: Docker for containerized deployment 🐋
- **Libraries**:
  - `Faker` for generating dummy data.
  - `fastapi-pagination` for paginated endpoints.
  - `pandas` for handling CSV exports and imports.
- **Testing and Development Tools**:
  - Docker Compose for environment setup.
  - Custom seed scripts for populating the database.

---

## 🛠️ 4. Installation

### ✅ Prerequisites
Before running the project, ensure the following are installed on your system:
- Python 3.9 or later.
- PostgreSQL (Ensure a running instance with access credentials).
- Docker and Docker Compose (optional for containerized environments).

### ⚙️ Setting Up the Project
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/Shiel000/employeeManager.git
   cd employeeManager
2. Build the Docker image:
   ```bash
    docker-compose build
3. Environment Variables: 
    The project already includes required environment variables (DATABASE_URL, MINIMUM_WAGE, etc.) in the docker-compose.yml file. No additional configuration is necessary unless modifications are required.
---
## 🚀 5. Running the Project
### ▶️ Start the Project
- Run the Docker container:
   ```bash
    docker-compose up

Access the API documentation via:
- Swagger: http://localhost:8001/docs
- Redoc: http://localhost:8001/redoc

### ℹ️ Notes
### 🌱 Seed the database
- Start the server and send a POST request to the following endpoint to populate the database with dummy data:
     ```http
     POST /api/populate/seed-data
     ```
   - Simply hitting this endpoint will populate the database with realistic test data, including employees, positions, salaries, etc. No additional configuration or changes are required.

---
## 📂 6.Data Structure

The database is structured to manage employees, positions, and payroll efficiently. Below is an overview of the main entities and their relationships.

#### **Entities:**
1. **Employees**: Stores employee information, including personal details and entry date.
2. **EmployeePositions**: Represents the relationship between an employee and their assigned positions.
3. **Positions**: Represents job positions, such as roles within the company.
4. **DetailPositions**: Records salary details and their historical changes for each position.
5. **Payrolls**: Manages payroll data for each employee by period.

#### **ER Diagram**
The relationships between these entities are as follows:


![er diagram](image.png)


### 🛠️ API Usage
For detailed examples of how to consume the API, please refer to the Swagger documentation. It provides comprehensive information about all endpoints, including request formats, parameters, and sample responses.

- **Swagger UI**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **Redoc**: [http://localhost:8001/redoc](http://localhost:8001/redoc)

### 📖 Additional Documentation

For detailed guides and advanced use cases, check out the [Project Wiki](https://github.com/Shiel000/employeeManager/wiki).
