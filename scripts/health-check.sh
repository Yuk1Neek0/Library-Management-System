#!/bin/bash

# Health check script for Library Management System
# Usage: ./health-check.sh [environment]

ENVIRONMENT=${1:-production}
BACKEND_URL=${BACKEND_URL:-http://localhost:5000}
FRONTEND_URL=${FRONTEND_URL:-http://localhost:80}

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "Health Check - $ENVIRONMENT"
echo "========================================="

# Check backend health
echo -n "Backend health check... "
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health" || echo "000")

if [ "$BACKEND_STATUS" == "200" ]; then
    echo -e "${GREEN}OK${NC} (HTTP $BACKEND_STATUS)"
    BACKEND_OK=true
else
    echo -e "${RED}FAILED${NC} (HTTP $BACKEND_STATUS)"
    BACKEND_OK=false
fi

# Check frontend
echo -n "Frontend accessibility... "
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" || echo "000")

if [ "$FRONTEND_STATUS" == "200" ]; then
    echo -e "${GREEN}OK${NC} (HTTP $FRONTEND_STATUS)"
    FRONTEND_OK=true
else
    echo -e "${RED}FAILED${NC} (HTTP $FRONTEND_STATUS)"
    FRONTEND_OK=false
fi

# Check database connectivity (through backend)
echo -n "Database connectivity... "
DB_CHECK=$(curl -s "$BACKEND_URL/api/books" -H "Authorization: Bearer dummy" 2>&1 || echo "error")

if [[ $DB_CHECK != *"error"* ]] && [[ $DB_CHECK != *"Connection refused"* ]]; then
    echo -e "${GREEN}OK${NC}"
    DB_OK=true
else
    echo -e "${RED}FAILED${NC}"
    DB_OK=false
fi

# Check Docker containers (if running locally)
if command -v docker-compose &> /dev/null; then
    echo ""
    echo "Docker container status:"
    docker-compose ps
fi

# Summary
echo ""
echo "========================================="
echo "Health Check Summary"
echo "========================================="

if $BACKEND_OK && $FRONTEND_OK && $DB_OK; then
    echo -e "Overall status: ${GREEN}HEALTHY${NC}"
    exit 0
else
    echo -e "Overall status: ${RED}UNHEALTHY${NC}"
    echo ""
    echo "Failed components:"
    [ "$BACKEND_OK" = false ] && echo "  - Backend"
    [ "$FRONTEND_OK" = false ] && echo "  - Frontend"
    [ "$DB_OK" = false ] && echo "  - Database"
    exit 1
fi
