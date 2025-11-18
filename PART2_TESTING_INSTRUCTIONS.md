# Part 2: Automated Testing Setup

**Assigned Team Member:** Member 2
**Estimated Time:** 2-3 hours

## Overview
This part implements comprehensive automated testing for both backend (Python/Flask) and frontend (React) components, including unit tests, integration tests, and code coverage reporting.

## Files Created

### Backend Testing
1. `.github/workflows/test.yml` - GitHub Actions workflow for automated testing
2. `backend/pytest.ini` - Pytest configuration file
3. `backend/tests/__init__.py` - Test package initialization
4. `backend/tests/conftest.py` - Pytest fixtures and test configuration
5. `backend/tests/test_auth.py` - Authentication endpoint tests
6. `backend/tests/test_books.py` - Book management endpoint tests

### Frontend Testing
7. `frontend/vitest.config.js` - Vitest configuration
8. `frontend/src/setupTests.js` - Test environment setup
9. `frontend/src/__tests__/Navbar.test.jsx` - Navbar component tests
10. `frontend/src/__tests__/api.test.js` - API service tests
11. Updated `frontend/package.json` - Added test dependencies and scripts

## What This Part Does

### 1. Backend Testing (pytest)
- **Unit Tests**: Test individual API endpoints and functions
- **Test Coverage**: Measures code coverage with pytest-cov
- **Test Fixtures**: Reusable test data and authenticated clients
- **Database Mocking**: Uses temporary test database

### 2. Frontend Testing (Vitest + React Testing Library)
- **Component Tests**: Test React components in isolation
- **Service Tests**: Test API service layer
- **DOM Testing**: Test user interactions and rendering
- **Fast Execution**: Vitest provides faster test execution than Jest

### 3. Integration Testing
- **End-to-End API Tests**: Test the complete request-response cycle
- **Real Server Testing**: Starts Flask server and runs actual HTTP requests
- **Uses existing test_api.py**: Leverages your current integration test

### 4. Code Coverage
- **Coverage Reports**: Generates coverage reports for both backend and frontend
- **Codecov Integration**: Uploads coverage to Codecov (optional)

## Installation Instructions

### Step 1: Install Backend Testing Dependencies
```bash
cd backend
pip install pytest pytest-cov pytest-flask
```

### Step 2: Install Frontend Testing Dependencies
```bash
cd frontend
npm install
```

The package.json has been updated with all necessary testing libraries:
- `@testing-library/react` - React component testing utilities
- `@testing-library/jest-dom` - Custom Jest matchers for DOM
- `vitest` - Fast unit test framework
- `jsdom` - JavaScript DOM implementation
- `@vitest/ui` - Visual test UI
- `@vitest/coverage-v8` - Code coverage reporting

### Step 3: Run Backend Tests Locally

```bash
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage report
pytest --cov=. --cov-report=term --cov-report=html

# Run specific test function
pytest tests/test_auth.py::TestAuthentication::test_login_success
```

### Step 4: Run Frontend Tests Locally

```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run coverage
```

### Step 5: View Coverage Reports

**Backend Coverage:**
```bash
cd backend
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

**Frontend Coverage:**
```bash
cd frontend
npm run coverage
# Open coverage/index.html in browser
```

### Step 6: Commit and Push

```bash
git add .github/workflows/test.yml
git add backend/pytest.ini
git add backend/tests/
git add frontend/vitest.config.js
git add frontend/src/setupTests.js
git add frontend/src/__tests__/
git add frontend/package.json
git commit -m "Part 2: Add automated testing setup with pytest and vitest"
git push origin main
```

## Test Structure

### Backend Test Organization
```
backend/tests/
├── __init__.py           # Package initialization
├── conftest.py           # Shared fixtures
├── test_auth.py          # Authentication tests
└── test_books.py         # Book management tests
```

### Frontend Test Organization
```
frontend/src/__tests__/
├── Navbar.test.jsx       # Navbar component tests
└── api.test.js           # API service tests
```

## Verification

1. **Local Testing:**
   - Run `pytest` in backend directory - should see 15+ tests passing
   - Run `npm test` in frontend directory - should see tests passing

2. **GitHub Actions:**
   - Go to GitHub repository → Actions tab
   - See "Automated Testing" workflow running
   - Three jobs should execute: test-backend, test-frontend, integration-test

3. **Coverage Reports:**
   - Backend coverage should be visible in terminal
   - Frontend coverage generates HTML report
   - Codecov integration (optional) shows coverage trends

## Test Examples

### Backend Test Example (test_auth.py)
Tests cover:
- Health check endpoint
- User registration (success and duplicate email)
- User login (success and invalid credentials)
- Getting current user info (authorized and unauthorized)

### Frontend Test Example (Navbar.test.jsx)
Tests cover:
- Rendering navbar with user info
- Rendering navbar without user
- Showing admin links for admin users
- Hiding admin links for regular users

## Expected Results

### Backend Tests
```
========================= test session starts =========================
collected 15 items

tests/test_auth.py ........                                    [ 53%]
tests/test_books.py .......                                    [100%]

========================= 15 passed in 2.34s ==========================
```

### Frontend Tests
```
✓ src/__tests__/Navbar.test.jsx (4)
✓ src/__tests__/api.test.js (2)

Test Files  2 passed (2)
Tests  6 passed (6)
```

## Troubleshooting

### Issue: pytest not found
**Solution:** Run `pip install pytest pytest-cov pytest-flask` in backend directory

### Issue: ModuleNotFoundError in tests
**Solution:** Ensure conftest.py properly adds parent directory to sys.path

### Issue: Frontend tests fail with "Cannot find module"
**Solution:** Run `npm install` to install all dependencies from updated package.json

### Issue: Database initialization errors
**Solution:** The conftest.py creates a temporary database for each test run

### Issue: GitHub Actions tests fail
**Solution:** Check that all test files are committed and pushed to repository

## Adding More Tests

### Backend Test Template:
```python
def test_your_feature(client, auth_headers):
    """Test description"""
    response = client.get('/api/endpoint', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['key'] == 'expected_value'
```

### Frontend Test Template:
```javascript
test('component renders correctly', () => {
  render(<YourComponent />);
  expect(screen.getByText(/expected text/i)).toBeInTheDocument();
});
```

## Code Coverage Goals

- **Backend:** Aim for >70% code coverage
- **Frontend:** Aim for >60% code coverage
- **Critical paths:** 100% coverage for authentication and core features

## Next Steps

After completing Part 2, you'll have:
- ✅ Automated test execution on every push
- ✅ Unit tests for backend API endpoints
- ✅ Component tests for frontend
- ✅ Integration tests for end-to-end flows
- ✅ Code coverage reporting

Part 3 will build on this by adding Docker containerization and build automation.
