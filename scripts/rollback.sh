#!/bin/bash

# Rollback script for Library Management System
# Usage: ./rollback.sh [version]
# Example: ./rollback.sh v1.2.3

set -e  # Exit on error

VERSION=${1:-previous}
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "========================================="
echo "Library Management System Rollback"
echo "Target: $VERSION"
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

# Navigate to project directory
cd "$PROJECT_DIR"

# Confirm rollback
read -p "Are you sure you want to rollback to $VERSION? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    print_warning "Rollback cancelled."
    exit 0
fi

# Create backup of current state
print_info "Creating backup of current deployment..."
BACKUP_DIR="backups/backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup database
if [ -f "backend/library.db" ]; then
    cp backend/library.db "$BACKUP_DIR/"
    print_info "Database backed up to $BACKUP_DIR/library.db"
fi

# Stop current containers
print_info "Stopping current containers..."
docker-compose down

# Rollback using git
if [ "$VERSION" != "previous" ]; then
    print_info "Rolling back code to version $VERSION..."
    git checkout tags/$VERSION
else
    print_info "Rolling back to previous commit..."
    git checkout HEAD~1
fi

# Rebuild and restart
print_info "Rebuilding containers with rolled back code..."
docker-compose build --no-cache

print_info "Starting rolled back version..."
docker-compose up -d

# Wait for services
print_info "Waiting for services to start..."
sleep 10

# Health check
BACKEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health || echo "000")

if [ "$BACKEND_HEALTH" == "200" ]; then
    print_info "Rollback successful! Backend is healthy."
else
    print_error "Rollback health check failed!"
    print_error "Attempting to restore from backup..."

    # Restore database if health check fails
    if [ -f "$BACKUP_DIR/library.db" ]; then
        cp "$BACKUP_DIR/library.db" backend/library.db
        docker-compose restart backend
    fi

    exit 1
fi

echo ""
echo "========================================="
print_info "Rollback completed successfully!"
echo "========================================="
echo ""
print_warning "Remember to return to main branch if needed:"
echo "  git checkout main"
echo ""
