# GitHub Copilot Instructions for Code Review

## Review Guidelines
- Check for security vulnerabilities
- Ensure code follows Python best practices
- Verify database schema changes are backward compatible
- Check test coverage for new functionality
- Validate input sanitization and SQL injection prevention

## Project-Specific Rules
1. **Database**: SQLite with CHECK constraints
2. **Testing**: pytest with 80%+ coverage goal
3. **Code Style**: Black formatting, flake8 linting
4. **CLI**: User-friendly prompts with validation

## Areas to Focus
- ✅ Database schema integrity
- ✅ Error handling
- ✅ Test completeness
- ✅ Documentation updates
- ✅ Performance considerations

## Review Checklist
- [ ] Security review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Backward compatibility maintained
- [ ] Code follows project conventions