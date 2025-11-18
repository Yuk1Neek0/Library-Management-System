# 🧪 Testing CI/CD on CI/CD Branch - Complete Guide

## ✅ Yes! You Can Test Everything Before Merging

You can fully test the CI/CD pipeline on the `CI/CD` branch before merging to `main`. This guide shows you exactly how.

---

## 📋 What We Updated

I just updated all 4 GitHub Actions workflows to run on the `CI/CD` branch:
- ✅ `.github/workflows/ci.yml` - Now runs on CI/CD branch
- ✅ `.github/workflows/test.yml` - Now runs on CI/CD branch
- ✅ `.github/workflows/docker-build.yml` - Now runs on CI/CD branch
- ✅ `.github/workflows/deploy.yml` - Now runs on CI/CD branch

---

## 🎯 Complete Testing Process

### **Phase 1: Push Updated Workflows (1 minute)**

```bash
# Make sure you're on CI/CD branch
git checkout CI/CD

# Commit the workflow updates
git add .github/workflows/
git commit -m "Update workflows to run on CI/CD branch for testing"
git push origin CI/CD
```

**What happens:**
- GitHub receives your push
- All 4 workflows will trigger automatically
- You can watch them run in real-time

---

### **Phase 2: Watch GitHub Actions Run (5-10 minutes)**

#### Step 1: Go to GitHub Actions Page

Visit: https://github.com/Yuk1Neek0/Library-Management-System/actions

#### Step 2: You Should See 4 Workflows Running

1. **CI/CD Pipeline** (Linting)
   - Status: 🟡 Running → 🟢 Success
   - Time: ~1-2 minutes

2. **Automated Testing**
   - Status: 🟡 Running → 🟢 Success
   - Time: ~2-3 minutes

3. **Docker Build and Push**
   - Status: 🟡 Running → 🟢 Success
   - Time: ~3-5 minutes

4. **Deploy to Production**
   - Status: 🟡 Running → 🟢 Success
   - Time: ~2-3 minutes

#### Step 3: Click on Each Workflow to See Details

**Example: Click "CI/CD Pipeline"**
- See each step execute
- View logs in real-time
- Check for errors or warnings

**Example: Click "Automated Testing"**
- See pytest running backend tests
- See vitest running frontend tests
- View test results

**Example: Click "Docker Build and Push"**
- See Docker images building
- See images pushed to registry
- View build logs

---

### **Phase 3: Test Locally (10 minutes)**

While GitHub Actions is running, test on your local machine:

#### 3.1 Install Dependencies

```bash
# Backend dependencies
cd backend
pip install -r requirements.txt
pip install pytest pytest-cov pytest-flask flake8 pylint black
cd ..

# Frontend dependencies
cd frontend
npm install
cd ..
```

#### 3.2 Test Linting Locally

```bash
# Test Python linting
cd backend
flake8 .
pylint *.py
black --check .
cd ..

# Test JavaScript linting
cd frontend
npx eslint . --ext .js,.jsx
cd ..
```

**Expected result:** You'll see linting results (warnings are OK, this is just for code quality)

#### 3.3 Test Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=. --cov-report=term

cd ..
```

**Expected result:**
```
========================= test session starts =========================
collected 17 items

tests/test_auth.py ........                                    [ 47%]
tests/test_books.py .........                                  [100%]

========================= 17 passed in 2.34s ==========================
```

#### 3.4 Test Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm run coverage

cd ..
```

**Expected result:**
```
✓ src/__tests__/Navbar.test.jsx (4)
✓ src/__tests__/api.test.js (2)

Test Files  2 passed (2)
Tests  6 passed (6)
```

#### 3.5 Test Docker Build and Run

```bash
# Create .env file
cp .env.example .env

# Edit .env (IMPORTANT!)
# Windows: notepad .env
# Mac/Linux: nano .env

# Set these values in .env:
# SECRET_KEY=test-secret-key-for-testing
# JWT_SECRET_KEY=test-jwt-secret-for-testing

# Build Docker images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

**Expected result:**
```
NAME                COMMAND             SERVICE    STATUS
library-backend     "python app.py"     backend    Up (healthy)
library-frontend    "nginx -g..."       frontend   Up (healthy)
```

#### 3.6 Test Application Access

**Open your browser:**

1. **Frontend:** http://localhost:80
   - You should see the Library Management System login page

2. **Backend Health:** http://localhost:5000/health
   - You should see: `{"status": "healthy"}`

3. **Test Login:**
   - Go to http://localhost:80
   - Login with admin credentials:
     - Email: `admin@library.com`
     - Password: `admin123`

**Expected result:** You should be able to login and access the dashboard

#### 3.7 Stop Docker

```bash
# Stop services
docker-compose down

# Or stop and remove volumes (deletes database)
docker-compose down -v
```

---

### **Phase 4: Test Deployment Scripts (5 minutes)**

#### 4.1 Make Scripts Executable (Mac/Linux only)

```bash
chmod +x scripts/*.sh
```

#### 4.2 Test Health Check Script

```bash
./scripts/health-check.sh
```

**Expected output:**
```
=========================================
Health Check - production
=========================================
Backend health check... OK (HTTP 200)
Frontend accessibility... OK (HTTP 200)
Database connectivity... OK

Docker container status:
NAME                STATUS
library-backend     Up (healthy)
library-frontend    Up (healthy)

=========================================
Health Check Summary
=========================================
Overall status: HEALTHY
```

#### 4.3 Test Backup Script

```bash
./scripts/backup.sh
```

**Expected output:**
```
=========================================
Library Management System Backup
=========================================
[INFO] Creating backup in: backups/backup-20251118-120000
[INFO] Database backed up
[INFO] Environment file backed up
[INFO] Backup archive created: backup-20251118-120000.tar.gz
=========================================
Backup completed successfully!
=========================================
```

#### 4.4 Test Deploy Script

```bash
./scripts/deploy.sh production
```

**Expected output:**
```
=========================================
Library Management System Deployment
Environment: production
=========================================
[INFO] Stopping existing containers...
[INFO] Building Docker images...
[INFO] Starting services...
[INFO] Waiting for services to be healthy...
[INFO] Checking backend health...
[INFO] Backend is healthy (HTTP 200)
[INFO] Frontend is accessible (HTTP 200)
=========================================
Deployment completed successfully!
=========================================
```

---

### **Phase 5: Verify GitHub Actions Results (After workflows complete)**

#### 5.1 Check All Workflows Passed

Go to: https://github.com/Yuk1Neek0/Library-Management-System/actions

**You should see:**
- ✅ CI/CD Pipeline - Success
- ✅ Automated Testing - Success
- ✅ Docker Build and Push - Success
- ✅ Deploy to Production - Success (might be skipped if deploy conditions not met)

#### 5.2 Check Individual Workflow Details

**Click on "CI/CD Pipeline":**
- Should show: ✅ Lint Code - Success
- View logs to see linting results

**Click on "Automated Testing":**
- Should show: ✅ Backend Tests - Success
- Should show: ✅ Frontend Tests - Success
- Should show: ✅ Integration Tests - Success

**Click on "Docker Build and Push":**
- Should show: ✅ Build Backend - Success
- Should show: ✅ Build Frontend - Success
- Should show: ✅ Test Docker Compose - Success

#### 5.3 Check Docker Images Were Pushed

Go to: https://github.com/Yuk1Neek0?tab=packages

You should see:
- `library-management-system-backend`
- `library-management-system-frontend`

---

## 🎯 Testing Checklist

Use this checklist to track your testing:

### GitHub Actions (Online)
- [ ] Pushed workflow updates to CI/CD branch
- [ ] Watched "CI/CD Pipeline" workflow run
- [ ] Watched "Automated Testing" workflow run
- [ ] Watched "Docker Build and Push" workflow run
- [ ] All workflows completed successfully
- [ ] Reviewed workflow logs for errors

### Local Testing (Your Computer)
- [ ] Installed backend dependencies
- [ ] Installed frontend dependencies
- [ ] Ran Python linting (flake8, pylint, black)
- [ ] Ran JavaScript linting (ESLint)
- [ ] Ran backend tests (pytest) - 17 tests passed
- [ ] Ran frontend tests (vitest) - 6 tests passed
- [ ] Created .env file with secrets
- [ ] Built Docker images successfully
- [ ] Started services with docker-compose
- [ ] Accessed frontend at http://localhost:80
- [ ] Accessed backend health at http://localhost:5000/health
- [ ] Logged in to application successfully
- [ ] Tested health check script
- [ ] Tested backup script
- [ ] Tested deploy script
- [ ] Stopped Docker services

---

## 🐛 Troubleshooting Common Issues

### Issue 1: GitHub Actions Not Running

**Problem:** Workflows don't trigger after push

**Solution:**
```bash
# Verify workflows are in correct location
ls -la .github/workflows/

# Should see 4 files:
# ci.yml, test.yml, docker-build.yml, deploy.yml

# Verify you pushed to CI/CD branch
git branch
# Should show: * CI/CD

# Push again
git push origin CI/CD
```

### Issue 2: Tests Fail on GitHub but Pass Locally

**Problem:** Tests pass on your computer but fail on GitHub Actions

**Possible causes:**
- Missing dependencies
- Environment differences
- Database initialization issues

**Solution:**
1. Click on failed workflow
2. Read error messages in logs
3. Common fixes:
   - Update `requirements.txt`: `pip freeze > backend/requirements.txt`
   - Check pytest fixtures in `conftest.py`
   - Verify test data

### Issue 3: Docker Build Fails

**Problem:** `docker-compose build` fails

**Solutions:**

```bash
# Clean everything and rebuild
docker-compose down -v
docker system prune -a
docker-compose build --no-cache

# If still fails, check logs
docker-compose build --progress=plain

# Common issues:
# - Missing files (check .dockerignore)
# - Network issues (try again)
# - Syntax errors in Dockerfile
```

### Issue 4: Port Already in Use

**Problem:** `Error: port is already allocated`

**Solution:**

```bash
# Windows - Find and kill process
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

netstat -ano | findstr :80
taskkill /PID <process_id> /F

# Mac/Linux - Find and kill process
lsof -i :5000
kill -9 <process_id>

lsof -i :80
sudo kill -9 <process_id>

# Or change ports in docker-compose.yml
```

### Issue 5: Can't Access Frontend/Backend

**Problem:** http://localhost:80 or http://localhost:5000 not working

**Solution:**

```bash
# Check if containers are running
docker-compose ps

# Should show both containers "Up (healthy)"

# If not healthy, check logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart

# If still not working, rebuild
docker-compose down
docker-compose up --build
```

### Issue 6: Tests Fail Due to Database

**Problem:** Tests fail with database errors

**Solution:**
The test configuration uses a temporary database. If issues persist:

```bash
# Check backend/tests/conftest.py exists
ls backend/tests/conftest.py

# Re-run tests with verbose output
cd backend
pytest -v -s

# Check if SQLite is available
python -c "import sqlite3; print('SQLite OK')"
```

### Issue 7: ESLint or Prettier Errors

**Problem:** Frontend linting fails

**Solution:**

```bash
cd frontend

# Install dependencies
npm install

# Run ESLint with auto-fix
npx eslint . --ext .js,.jsx --fix

# If errors persist, check .eslintrc.json
cat ../.eslintrc.json
```

---

## 📊 Expected Test Results Summary

### GitHub Actions
- **CI/CD Pipeline:** ✅ Success (1-2 min)
- **Automated Testing:** ✅ Success (2-3 min)
- **Docker Build:** ✅ Success (3-5 min)
- **Deploy:** ✅ Success or ⚠️ Skipped (deployment conditions)

### Local Tests
- **Backend Tests:** 17 passed
- **Frontend Tests:** 6 passed
- **Total Tests:** 23 passed
- **Coverage:** >70%

### Docker
- **Backend Image:** Built successfully
- **Frontend Image:** Built successfully
- **Services:** Both healthy
- **Frontend:** Accessible at port 80
- **Backend:** Accessible at port 5000

---

## ✅ Success Criteria

Your CI/CD is working correctly if:

1. ✅ All GitHub Actions workflows complete successfully
2. ✅ All 23 tests pass (17 backend + 6 frontend)
3. ✅ Docker images build without errors
4. ✅ Docker containers start and become healthy
5. ✅ Frontend is accessible in browser
6. ✅ Backend health endpoint responds
7. ✅ You can login to the application
8. ✅ Deployment scripts run successfully

---

## 🎉 After Successful Testing

Once everything passes:

### Option 1: Merge to Main

```bash
git checkout main
git merge CI/CD
git push origin main
```

### Option 2: Create Pull Request

Visit: https://github.com/Yuk1Neek0/Library-Management-System/pull/new/CI/CD

---

## 📚 Quick Commands Reference

```bash
# GitHub Actions
git push origin CI/CD  # Trigger workflows

# Local Testing
pytest                 # Backend tests
npm test               # Frontend tests

# Docker
docker-compose build   # Build images
docker-compose up -d   # Start services
docker-compose ps      # Check status
docker-compose logs -f # View logs
docker-compose down    # Stop services

# Scripts
./scripts/health-check.sh  # Check health
./scripts/backup.sh        # Backup database
./scripts/deploy.sh        # Deploy
```

---

## 🆘 Need Help?

If you encounter issues:
1. Check this troubleshooting section
2. Review GitHub Actions logs
3. Check Docker logs: `docker-compose logs`
4. Create a GitHub issue
5. Review main documentation: [HOW_TO_USE_CICD.md](HOW_TO_USE_CICD.md)

---

**Happy Testing! 🧪 Everything should work perfectly on the CI/CD branch before you merge!** 🚀
