#!/bin/bash
# Quick test startup script - no database required for basic testing

echo "========================================="
echo "Starting Vehicle Database - Quick Test"
echo "========================================="
echo ""

# Start backend
echo "[1/2] Starting Backend API..."
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install
source venv/bin/activate
pip install -q fastapi uvicorn sqlalchemy pydantic pydantic-settings aiohttp 2>/dev/null

# Start API in background
echo "Starting API server at http://localhost:8000"
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../api.log 2>&1 &
API_PID=$!
echo "API running (PID: $API_PID)"

cd ..

# Give API time to start
sleep 3

# Test API
echo ""
echo "[2/2] Testing API..."
curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "API starting..."

echo ""
echo "========================================="
echo "✓ Backend Started!"
echo "========================================="
echo ""
echo "Access Points:"
echo "  - API Health: http://localhost:8000/health"
echo "  - API Docs:   http://localhost:8000/docs"
echo "  - API Root:   http://localhost:8000/"
echo ""
echo "View logs: tail -f api.log"
echo "Stop API:  kill $API_PID"
echo ""
echo "Note: Database features require PostgreSQL setup."
echo "See QUICKSTART.md for full setup instructions."
echo ""
