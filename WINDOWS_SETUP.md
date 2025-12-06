# Windows Setup Guide - Step by Step

Follow these steps to get the Vehicle Repair Database API running on Windows.

## Prerequisites

1. **Python 3.11+** - [Download from python.org](https://www.python.org/downloads/)
   - ✅ During installation, check "Add Python to PATH"

2. **PostgreSQL 15+** - [Download from postgresql.org](https://www.postgresql.org/download/windows/)
   - ✅ Remember the password you set during installation

3. **Git** - [Download from git-scm.com](https://git-scm.com/downloads)

4. **Redis (Optional)** - [Download from GitHub](https://github.com/microsoftarchive/redis/releases)
   - Or use Memurai (Redis for Windows): [Download from memurai.com](https://www.memurai.com/get-memurai)

---

## Step 1: Verify Installations

Open **Command Prompt** and run:

```cmd
python --version
psql --version
git --version
```

All should show version numbers.

---

## Step 2: Navigate to Your Project

```cmd
cd C:\Users\grand\ctc-jade.li
```

---

## Step 3: Set Up PostgreSQL Database

### Option A: Using pgAdmin (GUI - Easiest)

1. Open **pgAdmin 4** (installed with PostgreSQL)
2. Connect to your PostgreSQL server (use the password you set)
3. Right-click "Databases" → Create → Database
4. Name: `vehicle_db`
5. Owner: `postgres`
6. Click "Save"

### Option B: Using Command Line

```cmd
# Open PostgreSQL command prompt (from Start menu: "SQL Shell (psql)")
# Press Enter for defaults, then enter your password

# In the psql prompt:
CREATE DATABASE vehicle_db;
\q
```

---

## Step 4: Set Up Python Environment

```cmd
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) in your prompt now
```

---

## Step 5: Install Dependencies

```cmd
# Make sure venv is activated (you should see (venv) in prompt)
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**This will take 2-3 minutes.** You should see packages installing.

---

## Step 6: Create Environment Configuration

```cmd
# Copy the example file
copy .env.example .env

# Edit it with Notepad
notepad .env
```

**Update these lines in .env:**

```ini
# Change this!
ENVIRONMENT=development

# Generate a secret key (run this in a separate command prompt):
# python -c "import secrets; print(secrets.token_urlsafe(32))"
# Then paste the output here:
SECRET_KEY=PASTE_YOUR_GENERATED_KEY_HERE

# Update with your PostgreSQL password
DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/vehicle_db

# If you don't have Redis, set this to disable rate limiting:
RATE_LIMIT_ENABLED=false
```

**To generate SECRET_KEY**, open a **new** Command Prompt and run:

```cmd
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and paste it into `.env` as the SECRET_KEY value.

---

## Step 7: Initialize Database

```cmd
# Make sure you're in backend directory with venv activated

# Create database tables
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> abc123, Add authentication models and initial schema
```

**If you get an error:**
- Check PostgreSQL is running (search for "Services" in Windows, find "postgresql-x64-15")
- Verify DATABASE_URL in .env has the correct password
- Make sure the database "vehicle_db" exists

---

## Step 8: Create Admin User

Create a file: `backend\scripts\create_admin.py`

```python
"""Create initial admin user."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.base import SessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password

def create_admin():
    """Create admin user."""
    db = SessionLocal()

    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("❌ Admin user already exists!")
            return

        # Create admin user
        admin = User(
            email="admin@yourcompany.com",
            username="admin",
            hashed_password=hash_password("Admin123!"),
            full_name="System Administrator",
            role=UserRole.ADMIN,
            is_active=True,
            is_verified=True
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("✅ Admin user created successfully!")
        print(f"   Email: {admin.email}")
        print(f"   Username: {admin.username}")
        print("   Password: Admin123!")
        print("\n⚠️  CHANGE THE PASSWORD AFTER FIRST LOGIN!")

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
```

**Run it:**

```cmd
python scripts\create_admin.py
```

**Expected output:**
```
✅ Admin user created successfully!
   Email: admin@yourcompany.com
   Username: admin
   Password: Admin123!
```

---

## Step 9: Start the API Server

```cmd
# Make sure you're in backend directory with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['C:\\Users\\grand\\ctc-jade.li\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Starting Vehicle Repair Database API v1.0.0
INFO:     Environment: development
INFO:     Database connection pool initialized successfully
INFO:     Application startup complete.
```

**Don't close this window!** The server is running.

---

## Step 10: Test It!

Open a **new** Command Prompt (keep the server running) and test:

### Test 1: Health Check

```cmd
curl http://localhost:8000/health
```

**OR** open in your browser: http://localhost:8000/health

**Expected response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "Vehicle Repair Database API",
  "environment": "development"
}
```

### Test 2: API Documentation

Open in your browser: **http://localhost:8000/docs**

You should see the Swagger UI with all API endpoints!

### Test 3: Login

```cmd
curl -X POST http://localhost:8000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"password\":\"Admin123!\"}"
```

**Expected response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

## 🎉 SUCCESS!

Your API is now running at: **http://localhost:8000**

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Next Steps

1. **Change the admin password** immediately:
   - Go to http://localhost:8000/docs
   - Login with admin/Admin123!
   - Use `/api/v1/auth/change-password` endpoint

2. **Create regular users** via the registration endpoint

3. **Test the VIN decoder**: `/api/v1/vin/decode`

---

## Troubleshooting

### "Module not found" errors

```cmd
# Make sure venv is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Connection refused" database errors

```cmd
# Check PostgreSQL service is running
# Search Windows Start Menu for "Services"
# Find "postgresql-x64-15" and make sure it's running

# Or restart it:
net stop postgresql-x64-15
net start postgresql-x64-15
```

### Port 8000 already in use

```cmd
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (use the PID from above)
taskkill /PID <pid_number> /F

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

### "SECRET_KEY validation failed"

```cmd
# Generate new key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copy output and paste into .env file
```

---

## Stopping the Server

To stop the server, press `CTRL+C` in the Command Prompt where it's running.

To deactivate the virtual environment:

```cmd
deactivate
```

---

## Running in the Future

Every time you want to start the server:

```cmd
# 1. Navigate to project
cd C:\Users\grand\ctc-jade.li\backend

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Optional: Install Redis for Full Features

Download Memurai (Redis for Windows): https://www.memurai.com/get-memurai

After installing:

1. Start Memurai service
2. Update `.env`:
   ```
   REDIS_URL=redis://localhost:6379/0
   RATE_LIMIT_ENABLED=true
   ```
3. Restart your API server

---

**Need help?** Check the documentation:
- IMPLEMENTATION_SUMMARY.md
- SECURITY_FIXES.md
- Or visit http://localhost:8000/docs
