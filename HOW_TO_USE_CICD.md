# 🚀 How to Use CI/CD Pipeline - Complete Guide

## Table of Contents
1. [Quick Start](#quick-start)
2. [Understanding the CI/CD Pipeline](#understanding-the-cicd-pipeline)
3. [GitHub Actions Workflows](#github-actions-workflows)
4. [Local Development Workflow](#local-development-workflow)
5. [Testing Your Code](#testing-your-code)
6. [Docker Deployment](#docker-deployment)
7. [Production Deployment](#production-deployment)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Quick Start

### Step 1: Merge CI/CD Branch to Main

```bash
# Create a pull request from CI/CD branch to main
# Go to: https://github.com/Yuk1Neek0/Library-Management-System/pull/new/CI/CD

# OR merge directly (if you have permission)
git checkout main
git merge CI/CD
git push origin main
```

### Step 2: Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
pip install pytest pytest-cov pytest-flask flake8 pylint black
cd ..
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

### Step 3: Set Up Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and set your secrets
# On Windows: notepad .env
# On Mac/Linux: nano .env
```

Update these values in `.env`:
```env
SECRET_KEY=your-super-secret-key-here-change-this
JWT_SECRET_KEY=your-jwt-secret-key-here-change-this
```

### Step 4: Test Everything Works

```bash
# Test linting
cd backend && flake8 . && cd ..
cd frontend && npx eslint . --ext .js,.jsx && cd ..

# Test backend tests
cd backend && pytest && cd ..

# Test frontend tests
cd frontend && npm test && cd ..

# Test Docker (requires Docker Desktop)
docker-compose build
docker-compose up -d
# Visit http://localhost:80
docker-compose down
```

---

## Understanding the CI/CD Pipeline

### What is CI/CD?

**CI (Continuous Integration):** Automatically tests your code when you push to GitHub
**CD (Continuous Deployment):** Automatically deploys your code to production

### What Our Pipeline Does

```
Code Push → Linting → Testing → Docker Build → Deploy → Monitor
    ↓          ↓          ↓           ↓           ↓         ↓
  GitHub   Quality   Run Tests   Create      Deploy    Health
   Push    Checks    (15+ tests)  Images      Live      Checks
```

### Four Main Components

1. **Linting (Code Quality)**
   - Checks Python code style
   - Checks JavaScript code style
   - Runs automatically on every push

2. **Testing (Automated Tests)**
   - Runs 15+ backend tests
   - Runs frontend component tests
   - Generates coverage reports

3. **Docker (Containerization)**
   - Builds backend image
   - Builds frontend image
   - Pushes to GitHub Container Registry

4. **Deployment (Automation)**
   - Deploys to production
   - Runs health checks
   - Automatic rollback if fails

---

## GitHub Actions Workflows

### How GitHub Actions Work

Every time you push code to GitHub, GitHub Actions automatically runs workflows.

### Our 4 Workflows

#### 1. CI/CD Pipeline (Linting)
**File:** `.github/workflows/ci.yml`
**Triggers:** Push or PR to `main` or `develop`
**What it does:**
- Checks Python code with flake8 and pylint
- Checks JavaScript code with ESLint
- Formats check with black

**View results:**
Go to GitHub → Actions → "CI/CD Pipeline" workflow

#### 2. Automated Testing
**File:** `.github/workflows/test.yml`
**Triggers:** Push or PR to `main` or `develop`
**What it does:**
- Runs pytest on backend (15+ tests)
- Runs vitest on frontend
- Generates coverage reports
- Uploads to Codecov

**View results:**
Go to GitHub → Actions → "Automated Testing" workflow

#### 3. Docker Build and Push
**File:** `.github/workflows/docker-build.yml`
**Triggers:** Push to `main` or tag `v*`
**What it does:**
- Builds Docker images
- Pushes to GitHub Container Registry
- Tests docker-compose setup
- Caches builds for speed

**View results:**
Go to GitHub → Actions → "Docker Build and Push" workflow

#### 4. Deploy to Production
**File:** `.github/workflows/deploy.yml`
**Triggers:** Push to `main` or manual trigger
**What it does:**
- Pre-deployment checks
- Builds and pushes images
- Deploys to production
- Runs post-deployment tests
- Automatic rollback on failure

**View results:**
Go to GitHub → Actions → "Deploy to Production" workflow

### How to View Workflow Results

1. Go to your GitHub repository
2. Click on "Actions" tab at the top
3. See all workflow runs
4. Click on any run to see detailed logs

**Example URL:**
`https://github.com/Yuk1Neek0/Library-Management-System/actions`

---

## Local Development Workflow

### Daily Development Cycle

```bash
# 1. Create a feature branch
git checkout -b feature/my-new-feature

# 2. Make your changes to code
# Edit files in backend/ or frontend/

# 3. Test your changes locally
cd backend && pytest && cd ..  # Backend tests
cd frontend && npm test && cd ..  # Frontend tests

# 4. Check code quality
cd backend && flake8 . && black --check . && cd ..
cd frontend && npx eslint . --ext .js,.jsx && cd ..

# 5. Commit your changes
git add .
git commit -m "Add my new feature"

# 6. Push to GitHub
git push origin feature/my-new-feature

# 7. Create Pull Request on GitHub
# GitHub Actions will automatically run tests!

# 8. After PR is approved, merge to main
# Deployment will happen automatically!
```

### What Happens When You Push

1. **You push code** → GitHub receives your code
2. **GitHub Actions triggers** → Workflows start running
3. **Linting runs** → Checks code quality (1-2 minutes)
4. **Tests run** → Runs all tests (2-3 minutes)
5. **You get feedback** → Green ✅ or Red ❌
6. **If main branch** → Docker builds and deploys

---

## Testing Your Code

### Backend Testing (pytest)

```bash
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::TestAuthentication::test_login_success

# Run with coverage
pytest --cov=. --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

### Frontend Testing (vitest)

```bash
cd frontend

# Run all tests
npm test

# Run in watch mode (re-runs on file changes)
npm test -- --watch

# Run with UI
npm run test:ui

# Run with coverage
npm run coverage
```

### Writing New Tests

**Backend test example:**
```python
# backend/tests/test_my_feature.py
def test_my_new_feature(client, auth_headers):
    """Test my new feature"""
    response = client.get('/api/my-endpoint', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['data'] == 'expected_value'
```

**Frontend test example:**
```javascript
// frontend/src/__tests__/MyComponent.test.jsx
import { render, screen } from '@testing-library/react';
import MyComponent from '../components/MyComponent';

test('renders my component', () => {
  render(<MyComponent />);
  expect(screen.getByText(/expected text/i)).toBeInTheDocument();
});
```

---

## Docker Deployment

### Local Docker Development

#### Start Everything with Docker

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Access Your Application

- **Frontend:** http://localhost:80
- **Backend API:** http://localhost:5000
- **Health Check:** http://localhost:5000/health

#### Development with Hot Reload

For development, you might want to run backend and frontend normally (not in Docker):

```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

This allows for faster development with hot reloading.

### Docker Commands Reference

```bash
# Build specific service
docker-compose build backend
docker-compose build frontend

# Start services
docker-compose up         # Foreground
docker-compose up -d      # Background (detached)

# View logs
docker-compose logs                 # All services
docker-compose logs -f              # Follow logs
docker-compose logs -f backend      # Specific service
docker-compose logs --tail=100      # Last 100 lines

# Restart services
docker-compose restart
docker-compose restart backend

# Stop services
docker-compose stop         # Stop without removing
docker-compose down         # Stop and remove containers
docker-compose down -v      # Also remove volumes (deletes database!)

# Execute commands in containers
docker-compose exec backend bash
docker-compose exec frontend sh

# View running containers
docker-compose ps

# View resource usage
docker stats
```

### Troubleshooting Docker

```bash
# Remove all containers and rebuild from scratch
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up
```

---

## Production Deployment

### Method 1: Automated Deployment via GitHub Actions

**This happens automatically when you push to main!**

```bash
git checkout main
git merge feature/my-feature
git push origin main

# GitHub Actions will:
# 1. Run linting
# 2. Run tests
# 3. Build Docker images
# 4. Deploy to production
# 5. Run health checks
# 6. Rollback if anything fails
```

**Monitor deployment:**
Go to GitHub → Actions → Watch "Deploy to Production" workflow

### Method 2: Manual Deployment Script

```bash
# Deploy to production
./scripts/deploy.sh production

# Deploy with latest code from git
./scripts/deploy.sh production --pull

# Deploy using pre-built images from registry
./scripts/deploy.sh production --use-registry
```

### Method 3: Server Deployment (VPS/Cloud)

**On your production server:**

```bash
# SSH into server
ssh user@your-server.com

# Navigate to project
cd /opt/Library-Management-System

# Pull latest changes
git pull origin main

# Deploy
./scripts/deploy.sh production

# Check health
./scripts/health-check.sh
```

### Setting Up GitHub Secrets for Automated Deployment

To enable automated deployment to your server:

1. **Go to GitHub Repository → Settings → Secrets and variables → Actions**

2. **Add these secrets:**
   - `PRODUCTION_HOST` - Your server IP or domain
   - `PRODUCTION_USER` - SSH username
   - `SSH_PRIVATE_KEY` - Your SSH private key

3. **Enable SSH deployment in workflow:**
   - Edit `.github/workflows/deploy.yml`
   - Find "Deploy to production via SSH" step
   - Change `if: false` to `if: true`

4. **Push changes:**
   ```bash
   git add .github/workflows/deploy.yml
   git commit -m "Enable automated SSH deployment"
   git push origin main
   ```

---

## Monitoring and Maintenance

### Health Checks

```bash
# Check if everything is running
./scripts/health-check.sh

# Check specific URLs
BACKEND_URL=https://api.yourdomain.com \
FRONTEND_URL=https://yourdomain.com \
./scripts/health-check.sh production
```

**What it checks:**
- Backend health endpoint responds
- Frontend is accessible
- Database connectivity works
- Docker containers are healthy

### Viewing Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service
docker-compose logs -f backend

# View last 100 lines
docker-compose logs --tail=100 backend

# View logs since specific time
docker-compose logs --since 2024-01-01T10:00:00 backend
```

### Database Backups

```bash
# Create backup
./scripts/backup.sh

# Backups are stored in backups/ directory
# File name: backup-YYYYMMDD-HHMMSS.tar.gz
```

**Automatic backup rotation:** Script keeps last 5 backups

**Restore from backup:**
```bash
# Extract backup
cd backups
tar -xzf backup-20240101-120000.tar.gz

# Copy database back
cp backup-20240101-120000/library.db ../backend/

# Restart backend
docker-compose restart backend
```

### Rollback to Previous Version

```bash
# Rollback to previous commit
./scripts/rollback.sh previous

# Rollback to specific version tag
./scripts/rollback.sh v1.2.3
```

**What rollback does:**
1. Creates backup of current state
2. Checks out previous code version
3. Rebuilds containers
4. Restarts services
5. Verifies health

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: GitHub Actions workflow not running

**Check:**
1. Are workflow files in `.github/workflows/`?
2. Did you push to `main` or `develop` branch?
3. Go to Actions tab - any error messages?

**Solution:**
```bash
# Verify workflow files exist
ls -la .github/workflows/

# Check branch
git branch

# Push to trigger workflow
git push origin main
```

#### Issue: Tests failing on GitHub but passing locally

**Possible causes:**
- Missing dependencies in requirements.txt
- Environment variable differences
- Database initialization issues

**Solution:**
```bash
# Check workflow logs on GitHub
# Update requirements.txt if needed
pip freeze > backend/requirements.txt
git add backend/requirements.txt
git commit -m "Update dependencies"
git push
```

#### Issue: Docker build fails

**Check:**
```bash
# View build logs
docker-compose build --progress=plain

# Common issues:
# - Missing files (check .dockerignore)
# - Syntax errors in Dockerfile
# - Network issues (can't download dependencies)
```

**Solution:**
```bash
# Rebuild from scratch
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
```

#### Issue: Port already in use

**Error:** `Bind for 0.0.0.0:5000 failed: port is already allocated`

**Solution:**
```bash
# Windows - Find and kill process
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Linux/Mac - Find and kill process
lsof -i :5000
kill -9 <process_id>

# OR change port in docker-compose.yml
```

#### Issue: Database changes not reflected

**Solution:**
```bash
# Remove volumes and restart
docker-compose down -v
docker-compose up --build
```

#### Issue: Frontend can't reach backend API

**Check:**
1. Is backend container running? `docker-compose ps`
2. Can you access http://localhost:5000/health directly?
3. Check nginx.conf proxy configuration

**Solution:**
```bash
# Verify backend is accessible
curl http://localhost:5000/health

# Check nginx config in container
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf

# Restart services
docker-compose restart
```

---

## Best Practices

### Development Workflow

✅ **DO:**
- Create feature branches for new work
- Write tests for new features
- Run tests locally before pushing
- Use meaningful commit messages
- Keep commits small and focused
- Review your own code before requesting review

❌ **DON'T:**
- Push directly to main (use PRs)
- Skip writing tests
- Commit commented-out code
- Push sensitive data (passwords, API keys)
- Mix multiple features in one commit

### Commit Message Format

```bash
# Good commit messages
git commit -m "Add user authentication endpoint"
git commit -m "Fix book search pagination bug"
git commit -m "Update Docker configuration for production"

# Bad commit messages
git commit -m "fix"
git commit -m "changes"
git commit -m "asdf"
```

### Testing Best Practices

- **Write tests first** (Test-Driven Development)
- **Aim for >70% code coverage**
- **Test edge cases** (what happens with invalid input?)
- **Use descriptive test names**
- **Keep tests independent** (one test shouldn't depend on another)

### Docker Best Practices

- **Use .env file** for configuration (never hardcode secrets)
- **Don't commit .env** (use .env.example as template)
- **Keep images small** (use multi-stage builds)
- **Clean up regularly** (`docker system prune`)
- **Use volumes** for persistent data

### Security Best Practices

- **Never commit secrets** (.env, API keys, passwords)
- **Use strong SECRET_KEY** and JWT_SECRET_KEY
- **Keep dependencies updated** (`pip list --outdated`, `npm outdated`)
- **Review security alerts** on GitHub
- **Use HTTPS in production**
- **Enable CORS properly** (don't use `*` in production)

---

## Quick Reference Commands

### Git Commands
```bash
git checkout -b feature/name    # Create branch
git add .                       # Stage changes
git commit -m "message"         # Commit
git push origin branch-name     # Push
git merge branch-name           # Merge
```

### Testing
```bash
cd backend && pytest            # Backend tests
cd frontend && npm test         # Frontend tests
```

### Linting
```bash
cd backend && flake8 .          # Python linting
cd frontend && npx eslint .     # JS linting
```

### Docker
```bash
docker-compose build            # Build images
docker-compose up -d            # Start services
docker-compose logs -f          # View logs
docker-compose down             # Stop services
```

### Deployment
```bash
./scripts/deploy.sh             # Deploy
./scripts/health-check.sh       # Check health
./scripts/backup.sh             # Backup database
./scripts/rollback.sh previous  # Rollback
```

---

## Next Steps

### After Setting Up CI/CD

1. **Merge CI/CD branch to main:**
   ```bash
   git checkout main
   git merge CI/CD
   git push origin main
   ```

2. **Watch workflows run:**
   - Go to GitHub → Actions
   - See all 4 workflows execute

3. **Test local deployment:**
   ```bash
   docker-compose up
   ```

4. **Distribute work to team:**
   - Share `SEND_TO_TEAM.md` with team members
   - Each member works on their assigned part

5. **Set up production server (optional):**
   - Provision VPS (DigitalOcean, AWS, etc.)
   - Install Docker
   - Clone repository
   - Deploy with `./scripts/deploy.sh`

### Learning More

- **GitHub Actions:** https://docs.github.com/en/actions
- **Docker:** https://docs.docker.com/
- **Pytest:** https://docs.pytest.org/
- **Vitest:** https://vitest.dev/

---

## Need Help?

- **Check documentation files:**
  - [CI_CD_IMPLEMENTATION_GUIDE.md](CI_CD_IMPLEMENTATION_GUIDE.md)
  - [PART1_LINTING_INSTRUCTIONS.md](PART1_LINTING_INSTRUCTIONS.md)
  - [PART2_TESTING_INSTRUCTIONS.md](PART2_TESTING_INSTRUCTIONS.md)
  - [PART3_DOCKER_INSTRUCTIONS.md](PART3_DOCKER_INSTRUCTIONS.md)
  - [PART4_DEPLOYMENT_INSTRUCTIONS.md](PART4_DEPLOYMENT_INSTRUCTIONS.md)

- **Check GitHub Actions logs:** Repository → Actions tab

- **Create GitHub issue:** Report bugs or ask questions

---

**Congratulations! You now have a complete CI/CD pipeline!** 🎉

Every time you push code to GitHub, it will:
- ✅ Check code quality
- ✅ Run all tests
- ✅ Build Docker images
- ✅ Deploy automatically
- ✅ Monitor health

This is exactly how professional development teams work! 🚀
