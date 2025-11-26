# Part 3: Docker Build Setup - Team Member 3

## Your Task
Set up Docker containerization and automated Docker builds for both frontend and backend.

## Files You Need to Create/Modify

### 1. Create `.github/workflows/docker-build.yml`
Create this file with the following content:

```yaml
name: CI - Docker Build

on:
  push:
    branches: [ main, CI/CD ]
  pull_request:
    branches: [ main ]

jobs:
  docker-build-and-test:
    name: Build and Test Docker Images
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Build Backend Docker Image
      run: |
        docker build -f Dockerfile.backend -t library-backend:test .

    - name: Build Frontend Docker Image
      run: |
        docker build -f Dockerfile.frontend -t library-frontend:test .

    - name: Test Docker Compose
      run: |
        docker compose up -d
        echo "Waiting for services to be healthy..."

        # Wait for services to be healthy (max 2 minutes)
        TIMEOUT=120
        ELAPSED=0
        INTERVAL=5

        while [ $ELAPSED -lt $TIMEOUT ]; do
          # Check if both containers are healthy
          BACKEND_HEALTH=$(docker inspect --format='{{.State.Health.Status}}' $(docker compose ps -q backend) 2>/dev/null || echo "not_found")
          FRONTEND_HEALTH=$(docker inspect --format='{{.State.Health.Status}}' $(docker compose ps -q frontend) 2>/dev/null || echo "not_found")

          echo "Backend health: $BACKEND_HEALTH"
          echo "Frontend health: $FRONTEND_HEALTH"

          if [ "$BACKEND_HEALTH" = "healthy" ] && [ "$FRONTEND_HEALTH" = "healthy" ]; then
            echo "Both services are healthy!"
            docker compose ps
            docker compose logs
            docker compose down
            exit 0
          fi

          sleep $INTERVAL
          ELAPSED=$((ELAPSED + INTERVAL))
          echo "Elapsed time: ${ELAPSED}s / ${TIMEOUT}s"
        done

        echo "Timeout waiting for services to be healthy"
        docker compose ps
        docker compose logs
        docker compose down
        exit 1
```

### 2. Create `Dockerfile.backend`
Create this file in the project root:

```dockerfile
# Backend Dockerfile for Flask Application
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Initialize database
RUN python database.py

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "app.py"]
```

### 3. Create `Dockerfile.frontend`
Create this file in the project root:

```dockerfile
# Multi-stage build for React frontend

# Stage 1: Build the React application
FROM node:18-alpine AS builder

WORKDIR /app

# Accept build argument for API URL
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Copy package files
COPY frontend/package*.json ./

# Install dependencies (including dev dependencies for build tools like vite)
RUN npm ci

# Copy source code
COPY frontend/ .

# Build the application (VITE_API_URL will be baked into the build)
RUN npm run build

# Stage 2: Serve with nginx
FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

### 4. Create `docker-compose.yml`
Create this file in the project root:

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: library-backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
    volumes:
      - backend_data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    container_name: library-frontend
    ports:
      - "80:80"
    depends_on:
      backend:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  backend_data:
```

### 5. Create `nginx.conf`
Create this file in the project root:

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript application/json;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Serve static files
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Note: API proxying removed for cloud deployments
    # Frontend will call backend directly using VITE_API_URL environment variable
    # This nginx config is optimized for serving the React SPA only
}
```

### 6. Create `.dockerignore`
Create this file in the project root:

```
# Git
.git
.gitignore

# Documentation
*.md
docs/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/

# Node
node_modules/
npm-debug.log
yarn-error.log
.npm
.yarn

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/

# Build
dist/
build/
*.egg

# Environment
.env
.env.local
.env.*.local

# Docker
docker-compose.override.yml

# CI/CD
.github/
```

## Steps to Complete

1. **Switch to main branch**:
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create a new feature branch**:
   ```bash
   git checkout -b feature/docker-setup
   ```

3. **Create all the files listed above** with the exact content

4. **Test Docker builds locally**:
   ```bash
   # Build backend
   docker build -f Dockerfile.backend -t library-backend:test .

   # Build frontend
   docker build -f Dockerfile.frontend -t library-frontend:test .

   # Test with docker compose
   docker compose up -d
   docker compose ps
   docker compose logs
   docker compose down
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add Docker build workflow and container configurations

   - Created GitHub Actions workflow for Docker builds
   - Added Dockerfile for backend (Python/Flask)
   - Added multi-stage Dockerfile for frontend (React/Nginx)
   - Created docker-compose.yml for local development
   - Added nginx configuration for serving React SPA
   - Added .dockerignore to optimize builds"
   ```

6. **Push to GitHub**:
   ```bash
   git push origin feature/docker-setup
   ```

7. **Create Pull Request** to main branch

## What This Does

- **Dockerfile.backend**: Packages the Flask backend into a Docker container
- **Dockerfile.frontend**: Builds React app and serves it with Nginx
- **docker-compose.yml**: Orchestrates both containers for local development
- **nginx.conf**: Configures web server for serving the React SPA
- **GitHub Actions**: Automatically builds and tests Docker images on every push

## Expected Result

After merging to main:
- Docker images will be built and tested automatically
- You can run the entire application with one command: `docker compose up`
- Both containers will have health checks to ensure they're running correctly

## Dependencies

This part can be worked on in parallel with Parts 1 and 2.
