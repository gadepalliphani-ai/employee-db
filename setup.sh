#!/bin/bash
# Setup script for Employee Database

set -e

echo "Setting up Employee Database..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python -c "from app import EmployeeDB; db = EmployeeDB('employee.db'); print('Database initialized.')"

# Run tests
echo "Running tests..."
pytest test_employee_db.py -v

echo ""
echo "Setup complete!"
echo ""
echo "To run the application:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "To run tests:"
echo "  pytest test_employee_db.py -v"