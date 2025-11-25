#!/bin/bash
# ============================================================================
# Vehicle Repair Database - Comprehensive Local Setup Script for Unix/Linux/Mac
# ============================================================================
# This script sets up the complete development environment
#
# Prerequisites:
#   - Python 3.11+ installed
#   - Node.js 18+ installed
#   - PostgreSQL 15+ installed and running
#   - Git installed
# ============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "========================================================================"
echo "Vehicle Repair Database - Unix/Linux/Mac Setup"
echo "========================================================================"
echo ""

# Check if running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
else
    OS="Linux"
fi

echo "Detected OS: $OS"
echo ""

# ============================================================================
# Step 1: Check Prerequisites
# ============================================================================
echo "========================================================================"
echo "[1/10] Checking prerequisites..."
echo "========================================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    echo "Install Python 3.11+ from https://www.python.org/downloads/"
    exit 1
fi
echo -e "${GREEN}✓ Python found:${NC}"
python3 --version

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}ERROR: Node.js is not installed${NC}"
    echo "Install Node.js 18+ from https://nodejs.org/"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found:${NC}"
node --version

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo -e "${YELLOW}WARNING: PostgreSQL command-line tools not found${NC}"
    echo "Continuing anyway, but you'll need to set up the database manually."
else
    echo -e "${GREEN}✓ PostgreSQL found:${NC}"
    psql --version
fi

# ============================================================================
# Step 2: Setup Environment Variables
# ============================================================================
echo ""
echo "========================================================================"
echo "[2/10] Setting up environment variables"
echo "========================================================================"
echo ""

if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo ""
    echo -e "${YELLOW}IMPORTANT: Edit .env file with your database credentials!${NC}"
    echo "Default database: postgresql://postgres:password@localhost:5432/vehicle_db"
else
    echo ".env file already exists, skipping..."
fi

# ============================================================================
# Step 3: Create PostgreSQL Database
# ============================================================================
echo ""
echo "========================================================================"
echo "[3/10] Creating PostgreSQL database"
echo "========================================================================"
echo ""

read -p "Do you want to create the database now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Creating database 'vehicle_db'..."

    # Try to create database
    if psql -U postgres -h localhost -c "CREATE DATABASE vehicle_db;" 2>/dev/null; then
        echo -e "${GREEN}✓ Database created successfully${NC}"
    else
        echo -e "${YELLOW}Note: Database may already exist or there was an error${NC}"
    fi

    # Create user (optional)
    psql -U postgres -h localhost -c "CREATE USER vehicle_user WITH PASSWORD 'vehicle_pass';" 2>/dev/null || true
    psql -U postgres -h localhost -c "GRANT ALL PRIVILEGES ON DATABASE vehicle_db TO vehicle_user;" 2>/dev/null || true

    echo -e "${GREEN}✓ Database setup complete${NC}"
else
    echo "Skipping database creation."
fi

# ============================================================================
# Step 4: Setup Python Virtual Environment
# ============================================================================
echo ""
echo "========================================================================"
echo "[4/10] Setting up Python virtual environment"
echo "========================================================================"
echo ""

cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# ============================================================================
# Step 5: Install Python Dependencies
# ============================================================================
echo ""
echo "========================================================================"
echo "[5/10] Installing Python dependencies"
echo "========================================================================"
echo ""

echo "Installing backend dependencies (this may take a few minutes)..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# ============================================================================
# Step 6: Setup Database Schema
# ============================================================================
echo ""
echo "========================================================================"
echo "[6/10] Setting up database schema"
echo "========================================================================"
echo ""

read -p "Do you want to run database migrations? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running database migrations..."

    # Initialize Alembic if not already done
    if [ ! -d "alembic" ]; then
        echo "Initializing Alembic..."
        alembic init alembic
    fi

    # Run migrations
    alembic upgrade head

    echo -e "${GREEN}✓ Database migrations completed${NC}"
else
    echo "Skipping migrations"
fi

# ============================================================================
# Step 7: Populate Database
# ============================================================================
echo ""
echo "========================================================================"
echo "[7/10] Populating database with sample data"
echo "========================================================================"
echo ""

read -p "Do you want to populate the database with sample data? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Fetching data from NHTSA and EPA APIs..."
    echo "This may take 5-10 minutes..."

    cat > populate_db.py << 'EOF'
import asyncio
from app.db.base import SessionLocal
from app.services.data_scraper import AutomotiveDataScraper

async def main():
    db = SessionLocal()
    scraper = AutomotiveDataScraper(db)
    await scraper.scrape_nhtsa_database(year_start=2020)
    db.close()

if __name__ == "__main__":
    asyncio.run(main())
EOF

    python populate_db.py
    rm populate_db.py

    echo -e "${GREEN}✓ Sample data imported${NC}"
else
    echo "Skipping data population"
fi

cd ..

# ============================================================================
# Step 8: Setup Frontend
# ============================================================================
echo ""
echo "========================================================================"
echo "[8/10] Setting up frontend"
echo "========================================================================"
echo ""

cd frontend

echo "Installing frontend dependencies (this may take a few minutes)..."
npm install

echo -e "${GREEN}✓ Frontend dependencies installed${NC}"

# Create frontend .env file
echo "VITE_API_URL=http://localhost:8000/api/v1" > .env.local
echo -e "${GREEN}✓ Frontend .env created${NC}"

cd ..

# ============================================================================
# Step 9: Run Tests
# ============================================================================
echo ""
echo "========================================================================"
echo "[9/10] Running tests"
echo "========================================================================"
echo ""

read -p "Do you want to run the test suite? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running backend tests..."
    cd backend
    source venv/bin/activate
    pytest tests/ -v
    cd ..
    echo -e "${GREEN}✓ Tests completed${NC}"
else
    echo "Skipping tests"
fi

# ============================================================================
# Step 10: Create Startup Scripts
# ============================================================================
echo ""
echo "========================================================================"
echo "[10/10] Creating startup scripts"
echo "========================================================================"
echo ""

# Create backend startup script
cat > start-backend.sh << 'EOF'
#!/bin/bash
echo "Starting Vehicle Repair Database Backend..."
cd backend
source venv/bin/activate
echo ""
echo "Backend API starting at http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF
chmod +x start-backend.sh
echo -e "${GREEN}✓ Created start-backend.sh${NC}"

# Create frontend startup script
cat > start-frontend.sh << 'EOF'
#!/bin/bash
echo "Starting Vehicle Repair Database Frontend..."
cd frontend
echo ""
echo "Frontend starting at http://localhost:3000"
echo ""
npm run dev
EOF
chmod +x start-frontend.sh
echo -e "${GREEN}✓ Created start-frontend.sh${NC}"

# Create Docker startup script
cat > start-docker.sh << 'EOF'
#!/bin/bash
echo "Starting Vehicle Repair Database with Docker..."
echo ""
echo "This will start all services using Docker Compose"
echo ""
docker-compose up -d
echo ""
echo "✓ Services started!"
echo ""
echo "Access points:"
echo "  Frontend:  http://localhost:3000"
echo "  Backend:   http://localhost:8000"
echo "  API Docs:  http://localhost:8000/docs"
echo "  Grafana:   http://localhost:3001 (admin/admin)"
echo ""
echo "View logs: docker-compose logs -f"
echo "Stop all:  docker-compose down"
EOF
chmod +x start-docker.sh
echo -e "${GREEN}✓ Created start-docker.sh${NC}"

# ============================================================================
# Setup Complete
# ============================================================================
echo ""
echo "========================================================================"
echo "Setup Complete!"
echo "========================================================================"
echo ""
echo "The Vehicle Repair Database has been set up successfully!"
echo ""
echo "Quick Start Options:"
echo ""
echo "  Option 1 - Local Development (Recommended for Development):"
echo "    Terminal 1: ./start-backend.sh"
echo "    Terminal 2: ./start-frontend.sh"
echo ""
echo "  Option 2 - Docker (Recommended for Testing):"
echo "    ./start-docker.sh"
echo "    (Requires Docker to be installed and running)"
echo ""
echo "Access Points:"
echo "  - Frontend:        http://localhost:3000"
echo "  - Backend API:     http://localhost:8000"
echo "  - API Docs:        http://localhost:8000/docs"
echo "  - ReDoc:           http://localhost:8000/redoc"
echo ""
echo "Next Steps:"
echo "  1. Edit .env file with your actual database credentials"
echo "  2. Run ./start-backend.sh and ./start-frontend.sh"
echo "  3. Visit http://localhost:3000 to start searching vehicles"
echo "  4. Check the API documentation at http://localhost:8000/docs"
echo ""
echo "For production deployment, see DEPLOYMENT.md"
echo ""
echo "========================================================================"
echo ""
