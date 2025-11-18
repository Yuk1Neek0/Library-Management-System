# ⚡ CI/CD Quick Start Guide

## 🎯 Get Started in 5 Minutes

### Step 1: Merge CI/CD Branch (30 seconds)

```bash
git checkout main
git merge CI/CD
git push origin main
```

**Or create a Pull Request:**
Visit: https://github.com/Yuk1Neek0/Library-Management-System/pull/new/CI/CD

---

### Step 2: Install Dependencies (2 minutes)

```bash
# Backend
cd backend
pip install -r requirements.txt
pip install pytest pytest-cov flake8 pylint black
cd ..

# Frontend
cd frontend
npm install
cd ..
```

---

### Step 3: Set Up Environment (1 minute)

```bash
# Copy template
cp .env.example .env

# Edit .env (Windows)
notepad .env

# Edit .env (Mac/Linux)
nano .env
```

**Set these values:**
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
```

---

### Step 4: Test It Works (1 minute)

```bash
# Test with Docker
docker-compose up -d

# Visit in browser:
# http://localhost:80 - Frontend
# http://localhost:5000/health - Backend health check

# Stop
docker-compose down
```

---

## ✅ That's It!

### Now What Happens?

Every time you push code to GitHub:
1. ✅ Code quality checks run automatically
2. ✅ All tests run automatically
3. ✅ Docker images build automatically
4. ✅ Deployment happens automatically (if configured)

### View Automated Workflows

Go to: https://github.com/Yuk1Neek0/Library-Management-System/actions

---

## 📚 Common Commands

### Development
```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, then commit
git add .
git commit -m "Add my feature"
git push origin feature/my-feature
```

### Testing
```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

### Docker
```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down
```

### Deployment
```bash
# Deploy to production
./scripts/deploy.sh production

# Check health
./scripts/health-check.sh

# Backup database
./scripts/backup.sh

# Rollback if needed
./scripts/rollback.sh previous
```

---

## 🎓 Team Member Tasks

Send each team member their files:

**Member 1:** Files from Part 1 + [PART1_LINTING_INSTRUCTIONS.md](PART1_LINTING_INSTRUCTIONS.md)
**Member 2:** Files from Part 2 + [PART2_TESTING_INSTRUCTIONS.md](PART2_TESTING_INSTRUCTIONS.md)
**Member 3:** Files from Part 3 + [PART3_DOCKER_INSTRUCTIONS.md](PART3_DOCKER_INSTRUCTIONS.md)
**Member 4:** Files from Part 4 + [PART4_DEPLOYMENT_INSTRUCTIONS.md](PART4_DEPLOYMENT_INSTRUCTIONS.md)

See [SEND_TO_TEAM.md](SEND_TO_TEAM.md) for details.

---

## 📖 Full Documentation

For complete details, see:
- **[HOW_TO_USE_CICD.md](HOW_TO_USE_CICD.md)** - Complete usage guide
- **[CI_CD_IMPLEMENTATION_GUIDE.md](CI_CD_IMPLEMENTATION_GUIDE.md)** - Implementation overview

---

## 🆘 Troubleshooting

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <pid> /F

# Mac/Linux
lsof -i :5000
kill -9 <pid>
```

**Docker issues:**
```bash
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up
```

**GitHub Actions not running:**
- Check you pushed to `main` or `develop` branch
- Go to Actions tab on GitHub
- Check workflow files are in `.github/workflows/`

---

## 🎉 Success!

You now have:
- ✅ Automated linting on every push
- ✅ Automated testing on every push
- ✅ Docker containerization
- ✅ Automated deployment
- ✅ Health monitoring
- ✅ Easy rollback

**Professional-grade CI/CD pipeline!** 🚀
