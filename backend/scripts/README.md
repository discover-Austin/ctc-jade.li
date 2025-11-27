# Database Management Scripts

This directory contains utility scripts for managing the Vehicle Repair Database.

## Scripts

### `init_db.py`

Initialize the database schema by creating all tables.

**Usage:**

```bash
# Create all tables
python scripts/init_db.py

# Drop all tables and recreate (WARNING: destroys all data)
python scripts/init_db.py --drop
```

**What it does:**
- Creates all database tables according to the SQLAlchemy models
- Sets up indexes and foreign key relationships
- Prints a list of all created tables

**Prerequisites:**
- Database server must be running
- `DATABASE_URL` must be set in `.env` or environment variables

---

### `seed_data.py`

Populate the database with sample vehicle data for testing and development.

**Usage:**

```bash
python scripts/seed_data.py
```

**What it does:**
- Creates sample vehicles with complete specifications:
  - 2020 Toyota Camry SE (complete with all subsystems)
  - 2019 Honda Accord Sport
  - 2021 Ford F-150 XLT
- Includes for each vehicle:
  - Engine and transmission specs
  - Electrical system specifications
  - Wheel and tire specs
  - Fluid specifications
  - Sample repair procedures (oil change, etc.)
  - Diagnostic trouble codes (DTCs)
  - Torque specifications
  - Maintenance schedules
  - Common problems

**Prerequisites:**
- Database must be initialized first (`init_db.py`)
- Will prompt before adding data if vehicles already exist

---

## Common Workflows

### First Time Setup

```bash
# 1. Start your database (PostgreSQL)
docker-compose up -d postgres

# 2. Initialize the database schema
cd backend
python scripts/init_db.py

# 3. Seed with sample data
python scripts/seed_data.py
```

### Reset Database

```bash
# WARNING: This destroys all data!
python scripts/init_db.py --drop
python scripts/seed_data.py
```

### Using Alembic (Migrations)

For schema changes after initial setup, use Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

---

## Environment Variables

These scripts use the following environment variables from `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:password@localhost:5432/vehicle_db` |
| `DB_POOL_SIZE` | Connection pool size | `10` |
| `DB_MAX_OVERFLOW` | Max overflow connections | `20` |

---

## Database Schema

The scripts create the following tables:

### Core Vehicle Tables
- `vehicles` - Vehicle registry
- `engines` - Engine specifications
- `transmissions` - Transmission specifications
- `suspension_systems` - Suspension and chassis
- `brake_systems` - Brake system specifications

### Electrical & Sensors
- `electrical_systems` - Electrical specifications
- `battery_specs` - Battery details
- `alternator_specs` - Alternator specifications
- `starter_specs` - Starter motor specs
- `wiring_diagrams` - Electrical schematics
- `sensor_specifications` - Sensor test procedures

### Fluids & Systems
- `fluid_specifications` - Fluid specs and capacities
- `hvac_systems` - Climate control specs
- `fuel_systems` - Fuel system specifications

### Wheels & Tires
- `wheel_tire_specs` - Wheel and tire specifications

### Repair & Maintenance
- `repair_procedures` - Step-by-step repair procedures
- `torque_specs` - Torque specifications
- `maintenance_schedules` - OEM maintenance intervals

### Diagnostics
- `diagnostic_codes` - DTC codes and procedures
- `obd2_pids` - OBD-II PID support
- `live_data_ranges` - Typical diagnostic data ranges

### Technical Information
- `technical_bulletins` - Manufacturer TSBs
- `recalls` - Safety recalls and campaigns
- `common_problems` - Community-reported issues

### Parts
- `parts_catalog` - OEM and aftermarket parts

**Total: 25+ tables**

---

## Troubleshooting

### "Connection refused" error

Ensure your PostgreSQL database is running:

```bash
docker-compose up -d postgres
```

### "Permission denied" error

Check your database user has create/drop privileges:

```sql
GRANT ALL PRIVILEGES ON DATABASE vehicle_db TO postgres;
```

### "Module not found" error

Ensure you're running from the `backend` directory:

```bash
cd backend
python scripts/init_db.py
```

### Tables already exist

If you want to recreate the schema:

```bash
python scripts/init_db.py --drop
```

---

## Adding Your Own Data

After seeding, you can add your own vehicles using the API:

```bash
# Start the API server
uvicorn app.main:app --reload

# Use the Swagger UI to add data
open http://localhost:8000/docs
```

Or use the database session directly in a Python script:

```python
from app.db.base import SessionLocal
from app.models.vehicle import Vehicle

db = SessionLocal()

new_vehicle = Vehicle(
    year=2022,
    make="Tesla",
    model="Model 3",
    trim="Long Range",
    # ... other fields
)

db.add(new_vehicle)
db.commit()
db.close()
```

---

## Further Reading

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
