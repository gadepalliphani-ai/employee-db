# Employee Database

A simple SQL-based employee database with unit testing and CI/CD pipeline.

## Features
- SQL database schema for employees, departments, and salaries
- Performance bonus tracking with analytics
- Python scripts for database operations
- Unit tests with pytest
- CI/CD pipeline with GitHub Actions
- Docker support

## Bonus Tracking Features
- Track performance bonuses alongside salary history
- Bonus analytics by employee and department
- Bonus percentage of salary calculations
- Historical bonus tracking with notes
- Input validation for bonus amounts

## Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run the application
python app.py
```

## Bonus Features Usage
```bash
# View bonus statistics
python app.py
# Choose option 5 for employee bonuses
# Choose option 6 for department bonuses

# Update salary with bonus
python app.py
# Choose option 8, then enter:
# - Employee ID
# - New Salary
# - 'y' for bonus
# - Bonus amount (validated)
# - Bonus notes (optional)
```

## Database Schema
See `schema.sql` for the database structure.