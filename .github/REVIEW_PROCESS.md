# Code Review Process

## Overview
All code changes must go through a review process before merging to main branch. This ensures code quality, security, and maintainability.

## Review Requirements

### 1. Minimum Requirements
- ✅ At least 1 approving review required
- ✅ All CI/CD checks must pass
- ✅ No merge conflicts
- ✅ Code follows project conventions

### 2. Who Can Review
- **Primary**: AI code review tools (GitHub Copilot, CodeRabbit, etc.)
- **Secondary**: Human reviewers (project maintainers)
- **Fallback**: Automated review via CI/CD with strict checks

### 3. Review Timeline
- **Small PRs** (< 200 lines): Within 24 hours
- **Medium PRs** (200-500 lines): Within 48 hours  
- **Large PRs** (> 500 lines): Within 72 hours

## Review Checklist

### Code Quality
- [ ] Code follows PEP 8 style guide
- [ ] Functions and classes have docstrings
- [ ] Type hints where appropriate
- [ ] No dead or commented-out code
- [ ] Error handling is comprehensive

### Testing
- [ ] Tests added for new functionality
- [ ] Existing tests still pass
- [ ] Test coverage maintained or improved
- [ ] Edge cases considered

### Security
- [ ] SQL injection prevention (parameterized queries)
- [ ] Input validation and sanitization
- [ ] No hardcoded secrets
- [ ] Error messages don't leak sensitive info

### Database
- [ ] Schema changes are backward compatible
- [ ] Migration scripts if needed
- [ ] Indexes for performance
- [ ] Constraints for data integrity

### Documentation
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Code comments where necessary
- [ ] Changelog updated

## AI Review Tools Setup

### GitHub Copilot
1. Install GitHub Copilot in your IDE
2. Enable Copilot Chat for code review
3. Use `.github/copilot-instructions.md` for project-specific guidance

### CodeRabbit
1. Install CodeRabbit GitHub App: https://github.com/apps/coderabbit
2. Configure with `.coderabbit.yaml`
3. CodeRabbit will auto-comment on PRs

### Other Tools
- **CodiumAI**: https://www.codium.ai
- **Sourcery**: https://sourcery.ai
- **SonarCloud**: https://sonarcloud.io

## Review Workflow

### Step 1: Create PR
```bash
git checkout -b feature-branch
# Make changes
git add . && git commit -m "Description"
git push origin feature-branch
# Create PR via GitHub UI or CLI
```

### Step 2: Request Reviews
1. **AI Review**: Tools auto-review when PR is created
2. **Human Review**: Add reviewers in GitHub PR sidebar
3. **Automated Checks**: CI/CD runs automatically

### Step 3: Address Feedback
1. Review comments from AI/human reviewers
2. Make requested changes
3. Push updates to branch
4. Re-request review if needed

### Step 4: Merge
1. Wait for required approvals
2. Ensure all checks pass
3. Squash and merge
4. Delete branch

## Emergency Bypass
In rare cases, emergency fixes can bypass review with:
1. `[EMERGENCY]` prefix in PR title
2. Explanation in PR description
3. Post-merge review within 24 hours

## Quality Metrics
- **Target**: 100% of PRs reviewed
- **Goal**: < 48 hour review cycle time
- **Standard**: < 5% of PRs require re-review

---

*Last updated: 2026-04-05*