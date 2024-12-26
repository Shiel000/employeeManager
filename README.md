# Employee Manager

## Problem Statement

The company "Y", a small SME, initially operated with around 10 employees. However, due to a significant increase in sales, they decided to hire more personnel. Unfortunately, they realized that traditional methods would not suffice to manage their growing workforce effectively.

### Proposed Solution

Through the implementation of an API, we aim to provide comprehensive management of all employees and activities related to them.

### Scope of the Problem

The company has requested a prototype system to decide whether to invest in its development. Therefore, we will narrow the problem domain. Instead of building various microservices, we will create a small sample service encompassing the primary activities related to employee management:

- **Creation and management of employees.**
- **Creation and management of different roles for employees.**
- **Creation and management of bonuses for employees.**
- **Creation and management of deductions for employees.**
- **Salary calculation for each employee.**

### Key Considerations

- Employees must have at least one role and a maximum of three (1 ≤ roles ≤ 3).
- Multiple employees can share the same role.
- Higher-ranking roles result in higher economic compensation.
- Deductions vary in severity, with greater deductions incurring larger financial penalties.
- Bonuses vary in type, with larger bonuses resulting in greater financial compensation.
- Salary calculation consists of:
  - A base salary (equal for all employees).
  - salarys associated with the employee’s roles.
  - Bonuses.
  - Years worked at the company.
  - Deductions.

This prototype will provide the necessary insights for the company to evaluate the feasibility of investing in a fully developed system.


## Commit Codes (for standardization):
    Add - comment (to add something)
    Fix - comment (to fix a bug)
    Edit - comment (to edit something)
    Delete - comment (to delete something)
