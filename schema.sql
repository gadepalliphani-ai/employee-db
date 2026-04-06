-- Employee Database Schema
-- Created: 2026-04-05

-- Departments table
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL UNIQUE,
    location TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Employees table
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    hire_date TEXT NOT NULL,
    job_title TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(department_id),
    manager_id INTEGER REFERENCES employees(employee_id),
    salary REAL CHECK (salary >= 0),
    work_mode TEXT CHECK (work_mode IN ('remote', 'in-person', 'hybrid')) DEFAULT 'in-person',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Salaries table (for salary history)
CREATE TABLE salaries (
    salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL REFERENCES employees(employee_id),
    salary REAL NOT NULL CHECK (salary >= 0),
    effective_date TEXT NOT NULL,
    end_date TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX idx_employees_department ON employees(department_id);
CREATE INDEX idx_employees_manager ON employees(manager_id);
CREATE INDEX idx_salaries_employee ON salaries(employee_id);
CREATE INDEX idx_salaries_dates ON salaries(effective_date, end_date);

-- Sample data
INSERT INTO departments (department_name, location) VALUES
    ('Engineering', 'San Francisco'),
    ('Sales', 'New York'),
    ('Marketing', 'Chicago'),
    ('HR', 'Austin'),
    ('Finance', 'Boston');

-- Sample employees
INSERT INTO employees (first_name, last_name, email, phone, hire_date, job_title, department_id, salary, work_mode) VALUES
    ('John', 'Doe', 'john.doe@company.com', '555-0101', '2023-01-15', 'Software Engineer', 1, 85000.00, 'hybrid'),
    ('Jane', 'Smith', 'jane.smith@company.com', '555-0102', '2022-03-20', 'Senior Engineer', 1, 110000.00, 'remote'),
    ('Bob', 'Johnson', 'bob.johnson@company.com', '555-0103', '2021-06-10', 'Sales Manager', 2, 95000.00, 'in-person'),
    ('Alice', 'Williams', 'alice.williams@company.com', '555-0104', '2020-11-05', 'Marketing Director', 3, 120000.00, 'hybrid'),
    ('Charlie', 'Brown', 'charlie.brown@company.com', '555-0105', '2023-08-22', 'HR Specialist', 4, 65000.00, 'in-person');

-- Update manager relationships
UPDATE employees SET manager_id = 2 WHERE employee_id = 1; -- John reports to Jane
UPDATE employees SET manager_id = 3 WHERE employee_id IN (4, 5); -- Alice and Charlie report to Bob

-- Sample salary history
INSERT INTO salaries (employee_id, salary, effective_date) VALUES
    (1, 85000.00, '2023-01-15'),
    (2, 110000.00, '2022-03-20'),
    (3, 95000.00, '2021-06-10'),
    (4, 120000.00, '2020-11-05'),
    (5, 65000.00, '2023-08-22');