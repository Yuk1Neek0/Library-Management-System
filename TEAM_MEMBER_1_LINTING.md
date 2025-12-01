# Part 1: Linting Setup - Team Member 1

## Your Task
Set up code linting for both frontend (JavaScript/React) and backend (Python/Flask).

## Files You Need to Create/Modify

### 1. Create `.github/workflows/ci.yml`
Create this file with the following content:

```yaml
name: CI - Linting

on:
  push:
    branches: [ main, CI/CD ]
  pull_request:
    branches: [ main ]

jobs:
  # Backend Linting
  lint-backend:
    name: Lint Backend (Python)
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      working-directory: ./backend
      run: |
        python -m pip install --upgrade pip
        pip install flake8

    - name: Lint with flake8
      working-directory: ./backend
      run: |
        # Stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # Exit-zero treats all errors as warnings
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

  # Frontend Linting
  lint-frontend:
    name: Lint Frontend (JavaScript/React)
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json

    - name: Install dependencies
      working-directory: ./frontend
      run: npm ci

    - name: Run ESLint
      working-directory: ./frontend
      run: npm run lint
```

### 2. Create `.flake8`
Create this file in the project root:

```ini
[flake8]
max-line-length = 127
exclude =
    .git,
    __pycache__,
    venv,
    env,
    .venv,
    node_modules,
    migrations,
    .pytest_cache
ignore = E203, W503
max-complexity = 10
```

### 3. Create `.pylintrc`
Create this file in the project root:

```ini
[MASTER]
disable=
    C0111, # missing-docstring
    C0103, # invalid-name
    R0903, # too-few-public-methods

[FORMAT]
max-line-length=127
```

### 4. Create `.eslintrc.json`
Create this file in the project root:

```json
{
  "env": {
    "browser": true,
    "es2021": true,
    "node": true,
    "jest": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react/jsx-runtime"
  ],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module",
    "ecmaFeatures": {
      "jsx": true
    }
  },
  "plugins": [
    "react"
  ],
  "rules": {
    "react/prop-types": "off",
    "no-unused-vars": "warn"
  },
  "settings": {
    "react": {
      "version": "detect"
    }
  }
}
```

### 5. Update `frontend/package.json`
Add the lint script to the scripts section:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "test": "jest"
  }
}
```

## Steps to Complete

1. **Switch to main branch**:
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create a new feature branch**:
   ```bash
   git checkout -b feature/linting-setup
   ```

3. **Create all the files listed above** with the exact content

4. **Test the linting locally**:
   ```bash
   # Test Python linting
   cd backend
   pip install flake8
   flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

   # Test JavaScript linting
   cd ../frontend
   npm ci
   npm run lint
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add linting workflow and configuration files

   - Created GitHub Actions workflow for linting (ci.yml)
   - Added flake8 configuration for Python backend
   - Added ESLint configuration for React frontend
   - Updated package.json with lint script"
   ```

6. **Push to GitHub**:
   ```bash
   git push origin feature/linting-setup
   ```

7. **Create Pull Request** to main branch and verify the workflow runs

## What This Does

- **Flake8**: Checks Python code for syntax errors, undefined names, and style issues
- **ESLint**: Checks JavaScript/React code for syntax errors, unused variables, and best practices
- **GitHub Actions**: Automatically runs these checks on every push and pull request

## Expected Result

After merging to main, every commit will trigger the linting workflow and you'll see a green checkmark if code follows standards.
