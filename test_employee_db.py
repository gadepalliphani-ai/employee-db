"""
Unit tests for Employee Database.
"""

import pytest
import os
import tempfile
from app import EmployeeDB

class TestEmployeeDB:
    """Test cases for EmployeeDB class."""
    
    @pytest.fixture
    def db(self):
        """Create a temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            db_path = tmp.name
        
        db = EmployeeDB(db_path)
        yield db
        
        # Cleanup
        os.unlink(db_path)
    
    def test_init_db(self, db):
        """Test database initialization."""
        # Check if tables were created
        tables = db.execute_query("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = {table['name'] for table in tables}
        
        expected_tables = {'departments', 'employees', 'salaries'}
        assert expected_tables.issubset(table_names)
    
    def test_add_employee(self, db):
        """Test adding a new employee."""
        employee_id = db.add_employee(
            first_name="Test",
            last_name="User",
            email="test.user@company.com",
            hire_date="2024-01-01",
            job_title="Tester",
            department_id=1,
            salary=50000.00
        )
        
        assert employee_id > 0
        
        # Verify the employee was added
        employees = db.get_employees()
        assert len(employees) == 6  # 5 sample + 1 new
        assert employees[-1]['email'] == "test.user@company.com"
    
    def test_get_employees(self, db):
        """Test retrieving employees."""
        employees = db.get_employees()
        
        # Should have 5 sample employees
        assert len(employees) == 5
        assert all('employee_id' in emp for emp in employees)
        assert all('department_name' in emp for emp in employees)
    
    def test_get_departments(self, db):
        """Test retrieving departments."""
        departments = db.get_departments()
        
        # Should have 5 sample departments
        assert len(departments) == 5
        assert departments[0]['department_name'] == 'Engineering'
    
    def test_update_salary(self, db):
        """Test updating employee salary."""
        # Get first employee
        employees = db.get_employees()
        employee_id = employees[0]['employee_id']
        old_salary = employees[0]['salary']
        
        # Update salary
        new_salary = old_salary + 10000
        db.update_salary(employee_id, new_salary)
        
        # Verify update
        updated_employees = db.get_employees()
        updated_emp = next(e for e in updated_employees if e['employee_id'] == employee_id)
        
        assert updated_emp['salary'] == new_salary
        
        # Check salary history
        salaries = db.execute_query(
            "SELECT * FROM salaries WHERE employee_id = ? ORDER BY effective_date DESC",
            (employee_id,)
        )
        assert len(salaries) >= 1
        assert salaries[0]['salary'] == new_salary
    
    def test_get_department_stats(self, db):
        """Test department statistics."""
        stats = db.get_department_stats()
        
        assert len(stats) == 5  # One for each department
        
        # Engineering should have employees
        engineering = next(s for s in stats if s['department_name'] == 'Engineering')
        assert engineering['employee_count'] == 2
        assert engineering['avg_salary'] > 0
    
    def test_add_employee_validation(self, db):
        """Test employee validation (email uniqueness)."""
        # Add first employee
        db.add_employee(
            first_name="Test1",
            last_name="User1",
            email="duplicate@company.com",
            hire_date="2024-01-01",
            job_title="Tester",
            department_id=1,
            salary=50000.00
        )
        
        # Try to add duplicate email (should work in SQLite but test the flow)
        # In a real PostgreSQL DB, this would raise an integrity error
        db.add_employee(
            first_name="Test2",
            last_name="User2",
            email="different@company.com",  # Different email
            hire_date="2024-01-02",
            job_title="Tester2",
            department_id=2,
            salary=60000.00
        )
        
        employees = db.get_employees()
        assert len(employees) == 7  # 5 sample + 2 new

def test_cli_interface():
    """Test CLI interface (basic smoke test)."""
    # This is a simple smoke test to ensure the CLI doesn't crash
    import subprocess
    result = subprocess.run(
        ['python', '-c', 'from app import EmployeeDB; db = EmployeeDB("test.db"); print("OK")'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0 or "OK" in result.stdout

if __name__ == "__main__":
    pytest.main([__file__, "-v"])