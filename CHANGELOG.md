# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-04-05

### Added
- Performance bonus tracking to salaries table
- Bonus analytics by employee and department
- Input validation for CLI prompts
- Enhanced documentation for bonus features

### Features
- Track performance bonuses with payment dates and notes
- Bonus percentage of salary calculations
- Department-level bonus statistics
- Employee-level bonus analytics
- Robust input validation for all CLI inputs

### Security
- Enhanced input validation for all numeric inputs
- Graceful error handling for invalid inputs
- SQL injection prevention via parameterized queries
- Input validation for bonus amounts (non-negative)

## [1.0.0] - 2026-04-05

### Added
- Initial release of Employee Database
- SQL database schema for employees, departments, and salaries
- Python CLI application for database management
- Unit tests with pytest
- CI/CD pipeline with GitHub Actions
- Docker support with Dockerfile and docker-compose
- Comprehensive documentation
- Setup script for easy installation

### Features
- Add, view, and update employees
- Department management
- Salary history tracking
- Department statistics
- Input validation
- SQLite database backend

### Security
- SQL injection prevention via parameterized queries
- Input validation
- Non-root Docker user