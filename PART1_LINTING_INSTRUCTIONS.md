# Part 1: Basic GitHub Actions Workflow and Linting

**Assigned Team Member:** Member 1
**Estimated Time:** 1-2 hours

## Overview
This part sets up the foundation of the CI/CD pipeline with GitHub Actions and implements code quality checks through linting for both backend (Python) and frontend (JavaScript/React).

## Files Created

1. `.github/workflows/ci.yml` - Main CI/CD workflow configuration
2. `.eslintrc.json` - ESLint configuration for JavaScript/React
3. `.flake8` - Flake8 configuration for Python
4. `.pylintrc` - Pylint configuration for Python

## What This Part Does

### 1. GitHub Actions Workflow
- Triggers on push and pull requests to `main` and `develop` branches
- Sets up Ubuntu runner environment
- Installs Python 3.8 and Node.js 18

### 2. Backend Linting (Python)
- **flake8**: Checks for Python syntax errors and code style issues
- **pylint**: Performs deeper code analysis for potential bugs
- **black**: Checks Python code formatting (PEP 8 compliance)

### 3. Frontend Linting (JavaScript/React)
- **ESLint**: Checks JavaScript and React code for errors and style issues
- Configured to work with React 18 and modern ES2021 syntax

## Installation Instructions

### Step 1: Install Python Linting Tools
```bash
cd backend
pip install flake8 pylint black
```

### Step 2: Install Frontend Linting Tools
```bash
cd frontend
npm install --save-dev eslint eslint-plugin-react
```

### Step 3: Test Linting Locally

#### Test Backend Linting:
```bash
cd backend

# Run flake8
flake8 .

# Run pylint
pylint *.py

# Check formatting with black
black --check .

# Auto-format with black (optional)
black .
```

#### Test Frontend Linting:
```bash
cd frontend

# Run ESLint
npx eslint . --ext .js,.jsx

# Auto-fix issues (optional)
npx eslint . --ext .js,.jsx --fix
```

### Step 4: Commit and Push
```bash
git add .github/workflows/ci.yml
git add .eslintrc.json
git add .flake8
git add .pylintrc
git commit -m "Part 1: Add GitHub Actions workflow and linting configuration"
git push origin main
```

## Verification

1. Go to your GitHub repository
2. Click on "Actions" tab
3. You should see the "CI/CD Pipeline" workflow running
4. The "Lint Code" job should execute and show results

## Expected Behavior

- Linting jobs will run but won't fail the build (using `continue-on-error: true`)
- This allows you to see code quality issues without blocking development
- You can later make these checks mandatory by removing `continue-on-error`

## Troubleshooting

### Issue: ESLint not found
**Solution:** Run `npm install --save-dev eslint eslint-plugin-react` in frontend directory

### Issue: Python linting tools not found
**Solution:** Run `pip install flake8 pylint black` in backend directory

### Issue: GitHub Actions workflow not triggering
**Solution:** Ensure the `.github/workflows/ci.yml` file is in the correct directory and pushed to GitHub

## Next Steps

After completing Part 1, you'll have:
- ✅ Basic GitHub Actions workflow
- ✅ Code quality checks for Python and JavaScript
- ✅ Foundation for adding more CI/CD stages

Part 2 will build on this by adding automated testing.
