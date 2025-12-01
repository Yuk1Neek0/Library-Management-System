#!/bin/bash

# Deployment script for Library Management System
# Usage: ./deploy.sh [environment]
# Example: ./deploy.sh production

set -e  # Exit on error

ENVIRONMENT=${1:-production}
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "========================================="
echo "Library Management System Deployment"
echo "Environment: $ENVIRONMENT"
echo "========================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Navigate to project directory
cd "$PROJECT_DIR"

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from .env.example..."
    cp .env.example .env
    print_warning "Please update .env file with your configuration before deploying."
    exit 1
fi

# Pull latest changes from git (optional)
if [ "$2" == "--pull" ]; then
    print_info "Pulling latest changes from git..."
    git pull origin main
fi

# Stop existing containers
print_info "Stopping existing containers..."
docker-compose down

# Pull latest images (if deploying from registry)
if [ "$2" == "--use-registry" ]; then
    print_info "Pulling latest images from registry..."
    docker-compose pull
else
    # Build new images
    print_info "Building Docker images..."
    docker-compose build --no-cache
fi

# Start services
print_info "Starting services..."
docker-compose up -d

# Wait for services to be healthy
print_info "Waiting for services to be healthy..."
sleep 10

# Check backend health
print_info "Checking backend health..."
BACKEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health || echo "000")

if [ "$BACKEND_HEALTH" == "200" ]; then
    print_info "Backend is healthy (HTTP $BACKEND_HEALTH)"
else
    print_error "Backend health check failed (HTTP $BACKEND_HEALTH)"
    docker-compose logs backend
    exit 1
fi

# Check frontend accessibility
print_info "Checking frontend accessibility..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:80 || echo "000")

if [ "$FRONTEND_STATUS" == "200" ]; then
    print_info "Frontend is accessible (HTTP $FRONTEND_STATUS)"
else
    print_warning "Frontend accessibility check failed (HTTP $FRONTEND_STATUS)"
    docker-compose logs frontend
fi

# Clean up old Docker images
print_info "Cleaning up old Docker images..."
docker image prune -f

# Show running containers
print_info "Running containers:"
docker-compose ps

echo ""
echo "========================================="
print_info "Deployment completed successfully!"
echo "========================================="
echo ""
echo "Services:"
echo "  - Backend:  http://localhost:5000"
echo "  - Frontend: http://localhost:80"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
