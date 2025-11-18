# Part 3: Build and Docker Containerization

**Assigned Team Member:** Member 3
**Estimated Time:** 2-3 hours

## Overview
This part containerizes the Library Management System using Docker, enabling consistent deployment across different environments. It includes multi-stage builds, docker-compose orchestration, and automated Docker image building through GitHub Actions.

## Files Created

1. `Dockerfile.backend` - Docker image for Flask backend
2. `Dockerfile.frontend` - Multi-stage Docker image for React frontend
3. `docker-compose.yml` - Orchestration for both services
4. `nginx.conf` - Nginx configuration for serving React app
5. `.dockerignore` - Files to exclude from Docker builds
6. `.env.example` - Environment variable template
7. `.github/workflows/docker-build.yml` - GitHub Actions for Docker builds

## What This Part Does

### 1. Backend Containerization
- **Base Image:** Python 3.8 slim (minimal footprint)
- **Dependencies:** Installs all Python packages from requirements.txt
- **Database:** Initializes SQLite database on container start
- **Health Check:** Automated health monitoring
- **Port:** Exposes 5000 for Flask API

### 2. Frontend Containerization
- **Multi-Stage Build:**
  - Stage 1: Build React app with Node.js
  - Stage 2: Serve static files with Nginx
- **Optimization:** Smaller final image (only includes built assets)
- **Nginx:** Configured for React Router and API proxying
- **Port:** Exposes 80 for web traffic

### 3. Docker Compose Orchestration
- **Services:** Backend and Frontend containers
- **Networking:** Private bridge network for inter-service communication
- **Volumes:** Persistent storage for SQLite database
- **Health Checks:** Automatic health monitoring and restart
- **Environment Variables:** Configurable through .env file

### 4. GitHub Actions Docker Build
- **Automatic Builds:** Triggered on push to main branch
- **Container Registry:** Pushes images to GitHub Container Registry (GHCR)
- **Versioning:** Tags images with branch, commit SHA, and semantic versions
- **Testing:** Tests docker-compose setup before deployment
- **Caching:** Uses GitHub Actions cache for faster builds

## Installation Instructions

### Prerequisites
Make sure you have Docker and Docker Compose installed:
```bash
# Check Docker installation
docker --version
docker-compose --version
```

### Step 1: Create Environment File
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and set your own secret keys
# On Linux/Mac:
# nano .env

# On Windows:
# notepad .env
```

Update these values in `.env`:
```env
SECRET_KEY=your-unique-secret-key-here
JWT_SECRET_KEY=your-unique-jwt-secret-here
```

### Step 2: Build Docker Images

```bash
# Build all services
docker-compose build

# Or build specific service
docker-compose build backend
docker-compose build frontend
```

### Step 3: Start Services

```bash
# Start all services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Step 4: Verify Services

```bash
# Check running containers
docker-compose ps

# Test backend health
curl http://localhost:5000/health

# Test frontend (in browser)
# Open http://localhost:80
```

### Step 5: Stop Services

```bash
# Stop all services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (deletes database!)
docker-compose down -v
```

## Docker Commands Reference

### Building
```bash
# Build without cache
docker-compose build --no-cache

# Build with progress output
docker-compose build --progress=plain

# Build specific service
docker-compose build backend
```

### Running
```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Start and rebuild
docker-compose up --build

# Scale services (not applicable for this setup)
docker-compose up --scale backend=2
```

### Managing
```bash
# List running containers
docker-compose ps

# View logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# Execute command in running container
docker-compose exec backend bash
docker-compose exec frontend sh

# Restart services
docker-compose restart

# Stop services
docker-compose stop

# Remove stopped containers
docker-compose rm
```

### Debugging
```bash
# Inspect backend container
docker-compose exec backend bash
cd /app
ls -la
python --version

# Inspect frontend container
docker-compose exec frontend sh
cd /usr/share/nginx/html
ls -la

# Check container health
docker inspect library-backend | grep -A 10 Health
docker inspect library-frontend | grep -A 10 Health

# View container resource usage
docker stats
```

## Testing Docker Locally

### Test Backend Container Alone
```bash
# Build backend image
docker build -f Dockerfile.backend -t library-backend:test .

# Run backend container
docker run -p 5000:5000 --name backend-test library-backend:test

# Test it
curl http://localhost:5000/health

# Stop and remove
docker stop backend-test
docker rm backend-test
```

### Test Frontend Container Alone
```bash
# Build frontend image
docker build -f Dockerfile.frontend -t library-frontend:test .

# Run frontend container
docker run -p 8080:80 --name frontend-test library-frontend:test

# Test it - open browser to http://localhost:8080

# Stop and remove
docker stop frontend-test
docker rm frontend-test
```

## GitHub Container Registry Setup

### Step 1: Enable GitHub Packages
The workflow is already configured to push to GitHub Container Registry (GHCR). It will automatically:
- Build images on push to main
- Tag with commit SHA and branch name
- Push to `ghcr.io/your-username/library-management-system-backend`
- Push to `ghcr.io/your-username/library-management-system-frontend`

### Step 2: Pull Images from GHCR
```bash
# Pull backend image
docker pull ghcr.io/your-username/library-management-system-backend:main

# Pull frontend image
docker pull ghcr.io/your-username/library-management-system-frontend:main

# Run from GHCR images
docker run -p 5000:5000 ghcr.io/your-username/library-management-system-backend:main
```

## Production Deployment Considerations

### Security
1. **Change default secrets** in `.env` file
2. **Use secrets management** (AWS Secrets Manager, Azure Key Vault, etc.)
3. **Enable HTTPS** with SSL certificates
4. **Configure CORS** properly for production domains
5. **Review nginx security headers** in nginx.conf

### Database
1. **Use PostgreSQL or MySQL** instead of SQLite for production
2. **Set up database backups** (volume snapshots)
3. **Use managed database service** (AWS RDS, Azure Database, etc.)

### Scaling
1. **Use orchestration platform** (Kubernetes, Docker Swarm)
2. **Add load balancer** for frontend and backend
3. **Implement caching** (Redis for sessions/tokens)
4. **Use CDN** for static assets

### Monitoring
1. **Add logging aggregation** (ELK stack, CloudWatch)
2. **Set up monitoring** (Prometheus, Grafana)
3. **Configure alerts** for health check failures
4. **Track performance metrics**

## Dockerfile Optimization

### Backend Dockerfile Features
- ✅ Slim base image (python:3.8-slim)
- ✅ Multi-layer caching (requirements.txt copied first)
- ✅ No cache for pip packages (--no-cache-dir)
- ✅ Cleanup of apt lists
- ✅ Health check endpoint
- ✅ Non-root user (could be added for extra security)

### Frontend Dockerfile Features
- ✅ Multi-stage build (builder + nginx)
- ✅ Alpine images (smallest size)
- ✅ Production-only dependencies (npm ci --only=production)
- ✅ Nginx for serving static files
- ✅ Custom nginx configuration
- ✅ Health check endpoint
- ✅ Gzip compression
- ✅ Security headers

## Troubleshooting

### Issue: Port already in use
```bash
# Find process using port 5000
# Linux/Mac:
lsof -i :5000

# Windows:
netstat -ano | findstr :5000

# Kill the process or change port in docker-compose.yml
```

### Issue: Database not initialized
```bash
# Remove volumes and restart
docker-compose down -v
docker-compose up --build
```

### Issue: Frontend can't connect to backend
```bash
# Check that both containers are on the same network
docker network ls
docker network inspect library-management-system_library-network

# Check nginx proxy configuration
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf
```

### Issue: Build fails due to missing dependencies
```bash
# Clear Docker cache and rebuild
docker system prune -a
docker-compose build --no-cache
```

### Issue: Container exits immediately
```bash
# Check logs for errors
docker-compose logs backend
docker-compose logs frontend

# Run container interactively to debug
docker-compose run --rm backend bash
docker-compose run --rm frontend sh
```

## Commit and Push

```bash
git add Dockerfile.backend Dockerfile.frontend
git add docker-compose.yml
git add nginx.conf
git add .dockerignore
git add .env.example
git add .github/workflows/docker-build.yml
git commit -m "Part 3: Add Docker containerization and build automation"
git push origin main
```

## Verification Checklist

After implementation, verify:

- [ ] Backend Docker image builds successfully
- [ ] Frontend Docker image builds successfully
- [ ] docker-compose up starts both services
- [ ] Backend health check returns 200 OK
- [ ] Frontend serves at http://localhost:80
- [ ] API calls from frontend reach backend
- [ ] Database persists data after container restart
- [ ] GitHub Actions workflow runs and builds images
- [ ] Images are pushed to GitHub Container Registry

## Next Steps

After completing Part 3, you'll have:
- ✅ Containerized backend and frontend applications
- ✅ Docker Compose orchestration
- ✅ Automated Docker image builds
- ✅ Container registry integration
- ✅ Production-ready container images

Part 4 will complete the CI/CD pipeline with deployment automation.
