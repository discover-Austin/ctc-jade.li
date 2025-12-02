#!/bin/bash
# =============================================================================
# Vehicle Repair Database - One-Command Launcher
# =============================================================================
# Just run: ./launch.sh
# Everything else is automatic!
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Clear screen for clean output
clear

echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        Vehicle Repair Database - Auto Launcher v1.0          ║
║                                                               ║
║        Just sit back... We'll handle everything! 🚀          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

# =============================================================================
# Auto-detect and setup
# =============================================================================

echo -e "${BLUE}[1/5]${NC} Checking environment..."

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}   → Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}   ✓ Configuration created${NC}"
else
    echo -e "${GREEN}   ✓ Configuration exists${NC}"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}   ✗ Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi
echo -e "${GREEN}   ✓ Python $(python3 --version | cut -d' ' -f2)${NC}"

# Check Node
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}   ⚠ Node.js not found - frontend won't be available${NC}"
    NODE_AVAILABLE=false
else
    echo -e "${GREEN}   ✓ Node.js $(node --version)${NC}"
    NODE_AVAILABLE=true
fi

# =============================================================================
# Setup backend
# =============================================================================

echo -e "\n${BLUE}[2/5]${NC} Setting up backend..."

cd backend

# Create/activate venv
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}   → Creating virtual environment...${NC}"
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies
if [ ! -f "venv/.deps_installed" ]; then
    echo -e "${YELLOW}   → Installing dependencies (first time only, ~2 min)...${NC}"
    pip install -q --upgrade pip 2>/dev/null
    pip install -q -r requirements.txt 2>/dev/null
    touch venv/.deps_installed
    echo -e "${GREEN}   ✓ Dependencies installed${NC}"
else
    echo -e "${GREEN}   ✓ Dependencies already installed${NC}"
fi

cd ..

# =============================================================================
# Setup frontend (if Node available)
# =============================================================================

if [ "$NODE_AVAILABLE" = true ]; then
    echo -e "\n${BLUE}[3/5]${NC} Setting up frontend..."

    cd frontend

    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}   → Installing npm packages (first time only, ~2 min)...${NC}"
        npm install --silent 2>/dev/null
        echo -e "${GREEN}   ✓ Packages installed${NC}"
    else
        echo -e "${GREEN}   ✓ Packages already installed${NC}"
    fi

    # Create frontend .env
    if [ ! -f ".env.local" ]; then
        echo "VITE_API_URL=http://localhost:8000/api/v1" > .env.local
    fi

    cd ..
else
    echo -e "\n${BLUE}[3/5]${NC} Skipping frontend (Node.js not available)"
fi

# =============================================================================
# Kill any existing processes
# =============================================================================

echo -e "\n${BLUE}[4/5]${NC} Cleaning up old processes..."

pkill -f "uvicorn app.main:app" 2>/dev/null && echo -e "${GREEN}   ✓ Stopped old backend${NC}" || echo -e "${GREEN}   ✓ No old backend running${NC}"
pkill -f "vite" 2>/dev/null && echo -e "${GREEN}   ✓ Stopped old frontend${NC}" || echo -e "${GREEN}   ✓ No old frontend running${NC}"

sleep 1

# =============================================================================
# Launch services
# =============================================================================

echo -e "\n${BLUE}[5/5]${NC} Launching services..."

# Start backend
cd backend
source venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo -e "${GREEN}   ✓ Backend started (PID: $BACKEND_PID)${NC}"

# Give backend time to start
sleep 3

# Start frontend if available
if [ "$NODE_AVAILABLE" = true ]; then
    cd frontend
    nohup npm run dev > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    echo -e "${GREEN}   ✓ Frontend started (PID: $FRONTEND_PID)${NC}"
fi

# =============================================================================
# Verify services
# =============================================================================

echo -e "\n${CYAN}Verifying services...${NC}"

# Check backend
sleep 2
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}   ✓ Backend API: ONLINE${NC}"
    BACKEND_STATUS="🟢 ONLINE"
else
    echo -e "${RED}   ✗ Backend API: FAILED${NC}"
    echo -e "${YELLOW}   Check logs/backend.log for details${NC}"
    BACKEND_STATUS="🔴 OFFLINE"
fi

# Check frontend
if [ "$NODE_AVAILABLE" = true ]; then
    sleep 2
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo -e "${GREEN}   ✓ Frontend: ONLINE${NC}"
        FRONTEND_STATUS="🟢 ONLINE"
    else
        echo -e "${YELLOW}   ⚠ Frontend: STARTING (wait ~10s)${NC}"
        FRONTEND_STATUS="🟡 STARTING"
    fi
else
    FRONTEND_STATUS="⚪ NOT AVAILABLE"
fi

# =============================================================================
# Success screen
# =============================================================================

clear

echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║                  ✓ Launch Complete! 🎉                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}\n"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Service Status:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
printf "  %-25s %s\n" "Backend API:" "$BACKEND_STATUS"
printf "  %-25s %s\n" "Frontend App:" "$FRONTEND_STATUS"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Access Your App:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if [ "$FRONTEND_STATUS" = "🟢 ONLINE" ] || [ "$FRONTEND_STATUS" = "🟡 STARTING" ]; then
    echo -e "  ${GREEN}➜${NC} ${YELLOW}Frontend:${NC}     http://localhost:3000"
fi
echo -e "  ${GREEN}➜${NC} ${YELLOW}API Docs:${NC}     http://localhost:8000/docs"
echo -e "  ${GREEN}➜${NC} ${YELLOW}API Root:${NC}     http://localhost:8000"
echo -e "  ${GREEN}➜${NC} ${YELLOW}Health Check:${NC} http://localhost:8000/health"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Useful Commands:${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  ${GREEN}View logs:${NC}        tail -f logs/backend.log"
echo -e "  ${GREEN}Stop services:${NC}    ./stop.sh"
echo -e "  ${GREEN}Restart:${NC}          ./launch.sh"
echo -e "  ${GREEN}Full setup:${NC}       ./setup-unix.sh"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

# Create logs directory if needed
mkdir -p logs

# Save PIDs for stop script
echo "$BACKEND_PID" > logs/backend.pid
[ "$NODE_AVAILABLE" = true ] && echo "$FRONTEND_PID" > logs/frontend.pid

echo -e "${GREEN}Services running in background. Logs in ./logs/${NC}\n"

# Auto-open browser if frontend is available
if [ "$FRONTEND_STATUS" = "🟢 ONLINE" ] || [ "$FRONTEND_STATUS" = "🟡 STARTING" ]; then
    echo -e "${YELLOW}Opening browser in 3 seconds...${NC}"
    sleep 3

    # Detect OS and open browser
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:3000 2>/dev/null &
    elif command -v open &> /dev/null; then
        open http://localhost:3000 2>/dev/null &
    fi
else
    echo -e "${YELLOW}Opening API docs in 3 seconds...${NC}"
    sleep 3

    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:8000/docs 2>/dev/null &
    elif command -v open &> /dev/null; then
        open http://localhost:8000/docs 2>/dev/null &
    fi
fi

echo ""
