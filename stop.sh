#!/bin/bash
# =============================================================================
# Vehicle Repair Database - Stop All Services
# =============================================================================

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "Stopping Vehicle Repair Database services..."
echo ""

# Kill processes by PID if available
if [ -f logs/backend.pid ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo -e "${GREEN}✓ Backend stopped (PID: $BACKEND_PID)${NC}"
    else
        echo -e "${YELLOW}⚠ Backend not running${NC}"
    fi
    rm -f logs/backend.pid
fi

if [ -f logs/frontend.pid ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo -e "${GREEN}✓ Frontend stopped (PID: $FRONTEND_PID)${NC}"
    else
        echo -e "${YELLOW}⚠ Frontend not running${NC}"
    fi
    rm -f logs/frontend.pid
fi

# Fallback: kill by process name
pkill -f "uvicorn app.main:app" 2>/dev/null && echo -e "${GREEN}✓ Killed uvicorn processes${NC}"
pkill -f "vite" 2>/dev/null && echo -e "${GREEN}✓ Killed vite processes${NC}"

echo ""
echo -e "${GREEN}All services stopped.${NC}"
echo ""
echo "To restart, run: ./launch.sh"
echo ""
