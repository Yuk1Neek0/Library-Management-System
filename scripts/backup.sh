#!/bin/bash

# Backup script for Library Management System
# Usage: ./backup.sh

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_BASE="$PROJECT_DIR/backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="$BACKUP_BASE/backup-$TIMESTAMP"

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

echo "========================================="
echo "Library Management System Backup"
echo "========================================="

# Create backup directory
mkdir -p "$BACKUP_DIR"
print_info "Creating backup in: $BACKUP_DIR"

# Backup database
if [ -f "$PROJECT_DIR/backend/library.db" ]; then
    cp "$PROJECT_DIR/backend/library.db" "$BACKUP_DIR/"
    print_info "Database backed up"
else
    print_warning "Database file not found"
fi

# Backup environment file
if [ -f "$PROJECT_DIR/.env" ]; then
    cp "$PROJECT_DIR/.env" "$BACKUP_DIR/"
    print_info "Environment file backed up"
fi

# Create backup archive
cd "$BACKUP_BASE"
tar -czf "backup-$TIMESTAMP.tar.gz" "backup-$TIMESTAMP"
rm -rf "backup-$TIMESTAMP"

print_info "Backup archive created: backup-$TIMESTAMP.tar.gz"

# Clean up old backups (keep last 5)
BACKUP_COUNT=$(ls -1 backup-*.tar.gz 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt 5 ]; then
    print_info "Cleaning up old backups (keeping last 5)..."
    ls -1t backup-*.tar.gz | tail -n +6 | xargs rm -f
fi

echo ""
echo "========================================="
print_info "Backup completed successfully!"
echo "========================================="
echo ""
echo "Backup location: $BACKUP_BASE/backup-$TIMESTAMP.tar.gz"
echo ""
