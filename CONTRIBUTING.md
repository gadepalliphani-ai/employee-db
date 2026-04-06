# Contributing to Employee Database

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/employee-db.git
   cd employee-db
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run tests**
   ```bash
   pytest test_employee_db.py -v
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## Code Style

- Use **Black** for code formatting
- Use **Flake8** for linting
- Write docstrings for all public functions and classes
- Add type hints where appropriate

## Testing

- Write unit tests for new functionality
- Maintain at least 80% code coverage
- Run tests before submitting PRs

## Pull Request Process

1. Create a feature branch from `main`
2. Add tests for your changes
3. Ensure all tests pass
4. Update documentation if needed
5. Submit a pull request

## Database Changes

If you modify the database schema:
1. Update `schema.sql`
2. Create migration scripts if needed
3. Update tests to reflect changes
4. Document the changes in `CHANGELOG.md`

## Security

- Never commit secrets or API keys
- Validate all user input
- Use parameterized queries to prevent SQL injection
- Follow the principle of least privilege