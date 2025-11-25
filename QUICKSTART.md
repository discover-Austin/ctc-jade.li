# 🚀 Quick Start Guide - Vehicle Repair Database

Get the Vehicle Repair Database running in **under 5 minutes**!

---

## Choose Your Deployment Method

### ⚡ Fastest: One-Click Deploy to Railway (RECOMMENDED)

**Time: 2 minutes** | **Cost: Free tier available**

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Run Deployment Script**
   - **Windows**: Double-click `deploy-railway.bat`
   - **Mac/Linux**:
     ```bash
     chmod +x deploy-railway.sh
     ./deploy-railway.sh
     ```

3. **Done!** Your app is live at `https://your-app.railway.app`

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

---

### 🎨 One-Click Deploy to Render

**Time: 3 minutes** | **Cost: Free tier available**

1. Click the button below:

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/your-org/vehicle-db)

2. Follow Render's setup wizard

3. Wait for deployment (3-5 minutes)

4. Access your app at `https://vehicle-db-api.onrender.com`

---

### 🐳 Docker (Local Development)

**Time: 5 minutes** | **Requirements: Docker Desktop**

#### Windows

1. Double-click `start-docker.bat`

2. Access the application:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000/docs

#### Mac/Linux

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

---

### 💻 Local Development (Manual)

**Time: 10 minutes** | **Requirements: Python 3.11+, Node.js 18+, PostgreSQL**

#### Windows

1. Double-click `setup-windows.bat`
2. Follow the installation wizard
3. Run `start-all.bat` to launch

#### Mac/Linux

```bash
# 1. Install backend dependencies
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Set up database
createdb vehicle_db
cp .env.example .env
# Edit .env with your database credentials

# 3. Run migrations
alembic upgrade head

# 4. Start backend
uvicorn app.main:app --reload

# 5. In a new terminal, install frontend
cd frontend
npm install
npm run dev
```

---

## Post-Installation Steps

### 1. Verify Installation

```bash
# Check API health
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","version":"1.0.0"}
```

### 2. Access the Application

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### 3. Populate Database (Optional)

```bash
# Using Railway/Render
railway run python scripts/populate_db.py

# Using Docker
docker-compose exec api python scripts/populate_db.py

# Using local setup
cd backend
python scripts/populate_db.py
```

This will import sample vehicle data from NHTSA (takes 5-10 minutes).

---

## First Search

1. Open http://localhost:3000

2. Search for a vehicle:
   - **Year**: 2020
   - **Make**: Toyota
   - **Model**: Camry

3. Click on a result to view:
   - Engine specifications
   - Transmission details
   - Repair procedures
   - Maintenance schedules
   - DTC codes

---

## Quick API Test

### Search Vehicles
```bash
curl "http://localhost:8000/api/v1/vehicles/search?year=2020&make=Toyota"
```

### Decode VIN
```bash
curl -X POST "http://localhost:8000/api/v1/vin/decode" \
  -H "Content-Type: application/json" \
  -d '{"vin":"1HGBH41JXMN109186"}'
```

### Get Torque Specs
```bash
# Replace {vehicle_id} with actual ID from search
curl "http://localhost:8000/api/v1/repair/torque-specs/{vehicle_id}"
```

### Lookup DTC Code
```bash
# Replace {vehicle_id} with actual ID
curl "http://localhost:8000/api/v1/diagnostic/dtc/{vehicle_id}/P0300"
```

---

## Troubleshooting

### Database Connection Error

**Problem**: `could not connect to server`

**Solution**:
```bash
# Check if PostgreSQL is running
# Windows
net start postgresql-x64-15

# Mac
brew services start postgresql

# Linux
sudo systemctl start postgresql

# Docker
docker-compose up -d postgres
```

### Port Already in Use

**Problem**: `Address already in use: 8000`

**Solution**:
```bash
# Find and kill the process
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Module Not Found

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Activate virtual environment first
cd backend
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate.bat  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### CORS Error in Frontend

**Problem**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution**: Update `backend/app/core/config.py`:
```python
BACKEND_CORS_ORIGINS = [
    "http://localhost:3000",
    "https://your-frontend-domain.com"
]
```

---

## Environment Variables

Create `.env` file in root directory:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/vehicle_db

# Redis (optional for local)
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000
```

---

## Next Steps

### For Developers

1. **Read the Documentation**
   - API Docs: http://localhost:8000/docs
   - Code: `README.md`
   - Contributing: `CONTRIBUTING.md`

2. **Run Tests**
   ```bash
   cd backend
   pytest tests/ -v
   ```

3. **Explore the API**
   - Use the interactive Swagger UI
   - Try different endpoints
   - Check response schemas

### For Production

1. **Deploy to Cloud**
   - See `DEPLOYMENT.md` for full guide
   - Railway (easiest): `deploy-railway.bat`
   - Render: Use `render.yaml`
   - AWS/GCP/Azure: See deployment guide

2. **Populate Real Data**
   - Import NHTSA vehicle database
   - Add repair procedures
   - Import OEM service manuals

3. **Configure Monitoring**
   - Set up Grafana dashboards
   - Configure error tracking
   - Enable performance monitoring

---

## Getting Help

### Documentation
- **README.md** - Project overview
- **DEPLOYMENT.md** - Deployment guide
- **CONTRIBUTING.md** - Contribution guidelines
- **API Docs** - http://localhost:8000/docs

### Support Channels
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@vehiclerepairdb.com

### Common Resources
- FastAPI Docs: https://fastapi.tiangolo.com
- React Docs: https://react.dev
- Material-UI: https://mui.com
- PostgreSQL: https://www.postgresql.org/docs/

---

## Success Checklist

✅ Application running locally
✅ Database connected
✅ Frontend accessible
✅ API returning data
✅ Tests passing
✅ Environment variables configured

**You're all set!** Start building or deploy to production.

---

## Deployment Comparison

| Method | Time | Difficulty | Cost | Best For |
|--------|------|------------|------|----------|
| **Railway** | 2 min | ⭐ Easy | Free-$20/mo | Quick deploy |
| **Render** | 3 min | ⭐ Easy | Free-$25/mo | Auto-deploy |
| **Docker** | 5 min | ⭐⭐ Medium | Free (local) | Development |
| **Manual** | 10 min | ⭐⭐⭐ Hard | Free (local) | Learning |
| **AWS** | 30 min | ⭐⭐⭐⭐⭐ Expert | $50+/mo | Production |

---

**Need help?** Open an issue or check the documentation!

Happy coding! 🚗💨
