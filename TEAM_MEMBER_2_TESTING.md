# Part 2: Testing Setup - Team Member 2

## Your Task
Set up automated testing for both frontend (Jest) and backend (Pytest).

## Files You Need to Create/Modify

### 1. Create `.github/workflows/test.yml`
Create this file with the following content:

```yaml
name: CI - Testing

on:
  push:
    branches: [ main, CI/CD ]
  pull_request:
    branches: [ main ]

jobs:
  # Backend Testing
  test-backend:
    name: Test Backend (Pytest)
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
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests with pytest
      working-directory: ./backend
      run: |
        pytest tests/ -v --tb=short

  # Frontend Testing
  test-frontend:
    name: Test Frontend (Jest)
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

    - name: Run tests with Jest
      working-directory: ./frontend
      run: npm test
```

### 2. Create `backend/pytest.ini`
Create this file in the backend directory:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### 3. Verify `backend/tests/__init__.py` exists
Make sure this file exists (it can be empty):

```python
# This file makes the tests directory a Python package
```

### 4. Verify `backend/tests/conftest.py` exists
Make sure this file has the pytest fixtures:

```python
import pytest
from app import create_app, db
from models import User, Book

@pytest.fixture
def app():
    """Create and configure a test application instance."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()
```

### 5. Update `frontend/package.json`
Make sure the test script is configured:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "test": "jest"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.1.5",
    "@testing-library/react": "^14.1.2",
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.55.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "jest": "^29.7.0",
    "jest-environment-jsdom": "^29.7.0",
    "vite": "^5.0.8"
  }
}
```

### 6. Verify `frontend/src/setupTests.js` exists
```javascript
import '@testing-library/jest-dom';

// learn more: https://github.com/testing-library/jest-dom
```

## Steps to Complete

1. **Switch to main branch**:
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create a new feature branch**:
   ```bash
   git checkout -b feature/testing-setup
   ```

3. **Create all the files listed above** with the exact content

4. **Test locally**:
   ```bash
   # Test backend
   cd backend
   pip install -r requirements.txt
   pip install pytest pytest-cov
   pytest tests/ -v

   # Test frontend
   cd ../frontend
   npm ci
   npm test
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add testing workflow and test configurations

   - Created GitHub Actions workflow for testing (test.yml)
   - Added pytest configuration for backend tests
   - Configured Jest for frontend tests
   - Added test fixtures and setup files"
   ```

6. **Push to GitHub**:
   ```bash
   git push origin feature/testing-setup
   ```

7. **Create Pull Request** to main branch

## What This Does

- **Pytest**: Runs Python unit tests for backend API endpoints
- **Jest**: Runs JavaScript tests for React components
- **GitHub Actions**: Automatically runs all tests on every push
- **Test Coverage**: Can be extended to show code coverage reports

## Expected Result

After merging to main, every commit will run all tests and you'll see which tests pass or fail.

## Dependencies

This part depends on Part 1 (Linting) being completed first, but can be worked on in parallel.
