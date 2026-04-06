#!/bin/bash
# Initialize GitHub repository for Employee Database

set -e

echo "Initializing GitHub repository..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git first."
    exit 1
fi

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Note: GitHub CLI (gh) is not installed."
    echo "You'll need to create the repository manually at: https://github.com/new"
    echo "Repository name: employee-db"
    echo "Description: Employee Database with SQL, testing, and CI/CD"
    echo "Initialize with README: No"
    echo ""
    echo "After creating the repository, run:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/employee-db.git"
    echo "  git push -u origin main"
    exit 0
fi

# Check if user is logged into GitHub CLI
if ! gh auth status &> /dev/null; then
    echo "Please log into GitHub CLI first:"
    echo "  gh auth login"
    exit 1
fi

# Create repository
echo "Creating GitHub repository..."
gh repo create employee-db \
    --description="Employee Database with SQL, testing, and CI/CD" \
    --public \
    --push \
    --source=. \
    --remote=origin

echo ""
echo "Repository created successfully!"
echo ""
echo "Next steps:"
echo "1. Set up secrets in GitHub repository settings:"
echo "   - DOCKER_USERNAME"
echo "   - DOCKER_PASSWORD"
echo "2. Enable GitHub Pages in settings (optional)"
echo "3. View CI/CD status at: https://github.com/$(gh api user --jq .login)/employee-db/actions"
echo ""
echo "To run locally:"
echo "  ./setup.sh"
echo "  python app.py"