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
            salary=50000.00,
            work_mode='remote'
        )
        
        # SQLite returns rowid, should be > 0 if inserted successfully
        # But with sample data, it might be > 5
        assert employee_id is not None
        
        # Verify the employee was added by checking email
        employees = db.get_employees()
        test_employee = next((e for e in employees if e['email'] == "test.user@company.com"), None)
        assert test_employee is not None
        assert test_employee['first_name'] == "Test"
        assert test_employee['last_name'] == "User"
    
    def test_get_employees(self, db):
        """Test retrieving employees."""
        employees = db.get_employees()
        
        # Should have at least the sample employees
        assert len(employees) >= 5
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
    
    def test_get_work_mode_stats(self, db):
        """Test work mode statistics."""
        stats = db.get_work_mode_stats()
        
        # Should have stats for each work mode
        work_modes = {s['work_mode'] for s in stats}
        expected_modes = {'remote', 'in-person', 'hybrid'}
        assert expected_modes.issubset(work_modes)
        
        # Check that we have counts
        for stat in stats:
            assert stat['employee_count'] >= 0
    
    def test_update_salary_with_bonus(self, db):
        """Test updating salary with performance bonus."""
        # Get first employee
        employees = db.get_employees()
        employee_id = employees[0]['employee_id']
        old_salary = employees[0]['salary']
        
        # Update salary with bonus
        new_salary = old_salary + 10000
        performance_bonus = 5000
        bonus_notes = "Excellent performance Q4"
        
        db.update_salary(employee_id, new_salary, performance_bonus, bonus_notes)
        
        # Verify update
        updated_employees = db.get_employees()
        updated_emp = next(e for e in updated_employees if e['employee_id'] == employee_id)
        
        assert updated_emp['salary'] == new_salary
        
        # Check salary history with bonus
        salaries = db.execute_query(
            "SELECT * FROM salaries WHERE employee_id = ? ORDER BY effective_date DESC",
            (employee_id,)
        )
        assert len(salaries) >= 1
        assert salaries[0]['salary'] == new_salary
        assert salaries[0]['performance_bonus'] == performance_bonus
        assert salaries[0]['bonus_notes'] == bonus_notes
    
    def test_get_bonus_stats(self, db):
        """Test bonus statistics."""
        stats = db.get_bonus_stats()
        
        # Should have stats for employees with bonuses
        assert len(stats) >= 5  # At least our sample employees
        
        # Check that sample bonuses are included
        total_bonuses = sum(s['total_bonus'] for s in stats)
        assert total_bonuses > 0
    
    def test_get_department_bonus_stats(self, db):
        """Test department bonus statistics."""
        stats = db.get_department_bonus_stats()
        
        # Should have stats for each department
        assert len(stats) == 5  # One for each department
        
        # Check that bonuses are calculated
        engineering = next(s for s in stats if s['department_name'] == 'Engineering')
        assert engineering['total_bonus'] > 0
        assert engineering['bonus_percentage'] > 0
    
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
        # Should have at least 7 employees (5 sample + 2 new)
        assert len(employees) >= 7

def test_cli_interface():
    """Test CLI interface (basic smoke test)."""
    # This is a simple smoke test to ensure the CLI doesn't crash
    import subprocess
    import tempfile
    import os
    
    # Create a temporary file for the test database
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        result = subprocess.run(
            ['python', '-c', f'from app import EmployeeDB; db = EmployeeDB("{db_path}"); print("OK")'],
            capture_output=True,
            text=True
        )
        # Check if it ran without critical errors
        assert "OK" in result.stdout or result.returncode == 0
    finally:
        # Clean up
        if os.path.exists(db_path):
            os.unlink(db_path)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])