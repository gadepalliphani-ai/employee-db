#!/usr/bin/env python3
"""
Employee Database Application
A simple CLI application to manage employee database.
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional
import sys

class EmployeeDB:
    """Employee database manager."""
    
    def __init__(self, db_path: str = "employee.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database with schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Read and execute schema
        with open('schema.sql', 'r') as f:
            schema = f.read()
        
        cursor.executescript(schema)
        conn.commit()
        conn.close()
        print(f"Database initialized at {self.db_path}")
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a query and return results as dictionaries."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                results = [dict(row) for row in cursor.fetchall()]
            else:
                conn.commit()
                results = []
            return results
        finally:
            conn.close()
    
    def add_employee(self, first_name: str, last_name: str, email: str, 
                    hire_date: str, job_title: str, department_id: int, 
                    salary: float, work_mode: str = 'in-person', 
                    phone: str = None, manager_id: int = None) -> int:
        """Add a new employee to the database."""
        query = """
        INSERT INTO employees 
        (first_name, last_name, email, phone, hire_date, job_title, department_id, manager_id, salary, work_mode)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (first_name, last_name, email, phone, hire_date, job_title, 
                 department_id, manager_id, salary, work_mode)
        
        self.execute_query(query, params)
        
        # Get the new employee ID
        result = self.execute_query("SELECT last_insert_rowid() as id")
        return result[0]['id']
    
    def get_employees(self, department_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all employees, optionally filtered by department."""
        if department_id:
            query = """
            SELECT e.*, d.department_name 
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.department_id
            WHERE e.department_id = ?
            ORDER BY e.last_name, e.first_name
            """
            return self.execute_query(query, (department_id,))
        else:
            query = """
            SELECT e.*, d.department_name 
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.department_id
            ORDER BY e.last_name, e.first_name
            """
            return self.execute_query(query)
    
    def get_departments(self) -> List[Dict[str, Any]]:
        """Get all departments."""
        return self.execute_query("SELECT * FROM departments ORDER BY department_name")
    
    def update_salary(self, employee_id: int, new_salary: float, performance_bonus: float = 0, 
                     bonus_notes: str = None):
        """Update an employee's salary and add to salary history with optional bonus."""
        # Update current salary
        query = "UPDATE employees SET salary = ? WHERE employee_id = ?"
        self.execute_query(query, (new_salary, employee_id))
        
        # Add to salary history
        query = """
        INSERT INTO salaries (employee_id, salary, performance_bonus, effective_date, bonus_notes)
        VALUES (?, ?, ?, date('now'), ?)
        """
        self.execute_query(query, (employee_id, new_salary, performance_bonus, bonus_notes))
    
    def get_department_stats(self) -> List[Dict[str, Any]]:
        """Get statistics for each department."""
        query = """
        SELECT 
            d.department_name,
            COUNT(e.employee_id) as employee_count,
            AVG(e.salary) as avg_salary,
            MIN(e.salary) as min_salary,
            MAX(e.salary) as max_salary
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id
        GROUP BY d.department_id, d.department_name
        ORDER BY d.department_name
        """
        return self.execute_query(query)
    
    def get_work_mode_stats(self) -> List[Dict[str, Any]]:
        """Get statistics by work mode."""
        query = """
        SELECT 
            COALESCE(work_mode, 'in-person') as work_mode,
            COUNT(employee_id) as employee_count,
            AVG(salary) as avg_salary,
            MIN(salary) as min_salary,
            MAX(salary) as max_salary
        FROM employees
        GROUP BY work_mode
        ORDER BY work_mode
        """
        return self.execute_query(query)
    
    def get_bonus_stats(self) -> List[Dict[str, Any]]:
        """Get bonus statistics."""
        query = """
        SELECT 
            e.employee_id,
            e.first_name || ' ' || e.last_name as employee_name,
            e.department_id,
            d.department_name,
            e.salary as current_salary,
            COALESCE(SUM(s.performance_bonus), 0) as total_bonus,
            COUNT(s.salary_id) as bonus_count,
            COALESCE(AVG(s.performance_bonus), 0) as avg_bonus,
            COALESCE(MAX(s.performance_bonus), 0) as max_bonus
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.department_id
        LEFT JOIN salaries s ON e.employee_id = s.employee_id AND s.performance_bonus > 0
        GROUP BY e.employee_id, e.first_name, e.last_name, e.department_id, d.department_name, e.salary
        ORDER BY total_bonus DESC, e.last_name, e.first_name
        """
        return self.execute_query(query)
    
    def get_department_bonus_stats(self) -> List[Dict[str, Any]]:
        """Get bonus statistics by department."""
        query = """
        SELECT 
            d.department_name,
            COUNT(DISTINCT e.employee_id) as employee_count,
            COALESCE(SUM(s.performance_bonus), 0) as total_bonus,
            COALESCE(AVG(s.performance_bonus), 0) as avg_bonus,
            COALESCE(MAX(s.performance_bonus), 0) as max_bonus,
            COALESCE(SUM(s.performance_bonus) * 100.0 / NULLIF(SUM(e.salary), 0), 0) as bonus_percentage
        FROM departments d
        LEFT JOIN employees e ON d.department_id = e.department_id
        LEFT JOIN salaries s ON e.employee_id = s.employee_id AND s.performance_bonus > 0
        GROUP BY d.department_id, d.department_name
        ORDER BY total_bonus DESC
        """
        return self.execute_query(query)

def main():
    """Main CLI interface."""
    db = EmployeeDB()
    
    print("Employee Database Management System")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. List all employees")
        print("2. List departments")
        print("3. View department statistics")
        print("4. View work mode statistics")
        print("5. View bonus statistics")
        print("6. View department bonus statistics")
        print("7. Add new employee")
        print("8. Update employee salary (with bonus)")
        print("9. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            employees = db.get_employees()
            print(f"\nTotal employees: {len(employees)}")
            for emp in employees:
                work_mode_display = emp.get('work_mode', 'in-person').title()
                print(f"{emp['employee_id']}: {emp['first_name']} {emp['last_name']} - {emp['job_title']} ({emp['department_name']}) - ${emp['salary']:,.2f} - {work_mode_display}")
        
        elif choice == '2':
            departments = db.get_departments()
            print("\nDepartments:")
            for dept in departments:
                print(f"{dept['department_id']}: {dept['department_name']} - {dept['location']}")
        
        elif choice == '3':
            stats = db.get_department_stats()
            print("\nDepartment Statistics:")
            for stat in stats:
                print(f"{stat['department_name']}: {stat['employee_count']} employees, "
                      f"Avg Salary: ${stat['avg_salary'] or 0:,.2f}")
        
        elif choice == '4':
            stats = db.get_work_mode_stats()
            print("\nWork Mode Statistics:")
            for stat in stats:
                print(f"{stat['work_mode'].title()}: {stat['employee_count']} employees, "
                      f"Avg Salary: ${stat['avg_salary'] or 0:,.2f}")
        
        elif choice == '5':
            stats = db.get_bonus_stats()
            print("\nBonus Statistics by Employee:")
            print(f"{'Name':<20} {'Department':<15} {'Salary':>12} {'Total Bonus':>12} {'Avg Bonus':>12}")
            print("-" * 75)
            for stat in stats:
                if stat['total_bonus'] > 0:
                    print(f"{stat['employee_name'][:19]:<20} {stat['department_name'][:14]:<15} "
                          f"${stat['current_salary']:>11,.2f} ${stat['total_bonus']:>11,.2f} "
                          f"${stat['avg_bonus']:>11,.2f}")
        
        elif choice == '6':
            stats = db.get_department_bonus_stats()
            print("\nBonus Statistics by Department:")
            print(f"{'Department':<20} {'Employees':>10} {'Total Bonus':>12} {'Avg Bonus':>12} {'% of Salary':>12}")
            print("-" * 75)
            for stat in stats:
                if stat['total_bonus'] > 0:
                    print(f"{stat['department_name'][:19]:<20} {stat['employee_count']:>10} "
                          f"${stat['total_bonus']:>11,.2f} ${stat['avg_bonus']:>11,.2f} "
                          f"{stat['bonus_percentage']:>11.1f}%")
        
        elif choice == '7':
            print("\nAdd New Employee:")
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone (optional): ").strip() or None
            hire_date = input("Hire Date (YYYY-MM-DD): ").strip()
            job_title = input("Job Title: ").strip()
            
            # Show departments
            departments = db.get_departments()
            print("\nAvailable Departments:")
            for dept in departments:
                print(f"{dept['department_id']}: {dept['department_name']}")
            
            department_id = int(input("Department ID: ").strip())
            salary = float(input("Salary: ").strip())
            work_mode = input("Work Mode (remote/in-person/hybrid, default: in-person): ").strip()
            if work_mode not in ['remote', 'in-person', 'hybrid']:
                work_mode = 'in-person'
            
            employee_id = db.add_employee(
                first_name, last_name, email, hire_date, job_title,
                department_id, salary, work_mode, phone
            )
            print(f"\nEmployee added successfully! ID: {employee_id}")
        
        elif choice == '8':
            employee_id = int(input("Employee ID: ").strip())
            new_salary = float(input("New Salary: ").strip())
            include_bonus = input("Include performance bonus? (y/n): ").strip().lower()
            
            performance_bonus = 0
            bonus_notes = None
            
            if include_bonus == 'y':
                performance_bonus = float(input("Performance Bonus Amount: ").strip())
                bonus_notes = input("Bonus Notes (optional): ").strip() or None
            
            db.update_salary(employee_id, new_salary, performance_bonus, bonus_notes)
            print("Salary updated successfully!")
        
        elif choice == '9':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()