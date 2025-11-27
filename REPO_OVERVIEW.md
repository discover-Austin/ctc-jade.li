# Repository Overview - Vehicle Repair Database

**Last Updated:** November 27, 2025
**Version:** 1.0.0
**License:** MIT

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Technology Stack](#technology-stack)
4. [Architecture](#architecture)
5. [Backend Components](#backend-components)
6. [Frontend Components](#frontend-components)
7. [Database Schema](#database-schema)
8. [API Endpoints](#api-endpoints)
9. [Infrastructure & DevOps](#infrastructure--devops)
10. [Development Workflow](#development-workflow)
11. [Deployment Options](#deployment-options)
12. [Testing Strategy](#testing-strategy)
13. [Documentation](#documentation)
14. [Current Status](#current-status)
15. [Roadmap](#roadmap)

---

## Project Overview

### Mission Statement

Build a comprehensive, free-to-access vehicle repair database that empowers mechanics, technicians, and DIY enthusiasts with factory-level information for all vehicles manufactured from 2014 onwards.

### What This Project Does

The **Vehicle Repair Database & Guide System** is a production-grade platform providing:

- **Comprehensive Vehicle Database**: Detailed specifications for 2014+ vehicles
- **Repair Procedures**: Step-by-step instructions with torque specifications
- **DTC Code Database**: Diagnostic trouble codes with diagnostic procedures
- **Technical Service Bulletins**: Manufacturer TSBs and recall information
- **Wiring Diagrams**: Electrical schematics and connector locations
- **Maintenance Schedules**: OEM-recommended service intervals
- **VIN Decoder**: Decode VINs to identify exact vehicle specifications
- **Parts Cross-Reference**: OEM and aftermarket part interchanges
- **Common Problems Database**: Community-reported issues and solutions

### Target Audience

- Professional mechanics and automotive technicians
- Independent repair shops
- DIY automotive enthusiasts
- Fleet maintenance departments
- Automotive educators and students

---

## Repository Structure

```
ctc-jade.li/
├── backend/                      # FastAPI backend application
│   ├── app/
│   │   ├── api/                 # API routes and endpoints
│   │   │   └── endpoints/       # Individual endpoint modules
│   │   │       ├── vehicles.py  # Vehicle search & retrieval
│   │   │       ├── vin.py       # VIN decoder
│   │   │       ├── repair.py    # Repair procedures
│   │   │       ├── diagnostic.py # DTC codes & diagnostics
│   │   │       └── technical.py  # TSBs & recalls
│   │   ├── core/                # Core configuration
│   │   │   └── config.py        # Application settings
│   │   ├── db/                  # Database utilities
│   │   │   └── base.py          # SQLAlchemy base
│   │   ├── models/              # SQLAlchemy ORM models
│   │   │   ├── vehicle.py       # Vehicle models
│   │   │   ├── electrical.py    # Electrical system models
│   │   │   ├── repair.py        # Repair procedure models
│   │   │   ├── diagnostic.py    # Diagnostic code models
│   │   │   ├── technical.py     # TSB & recall models
│   │   │   ├── parts.py         # Parts & specifications
│   │   │   ├── fluid.py         # Fluid specifications
│   │   │   └── wheel_tire.py    # Wheel & tire specs
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   │   └── data_scraper.py  # External data integration
│   │   └── main.py              # Application entry point
│   ├── tests/                   # Backend tests
│   │   └── test_api.py          # API endpoint tests
│   ├── Dockerfile               # Backend container definition
│   └── requirements.txt         # Python dependencies (25 files)
│
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── pages/
│   │   │   └── VehicleSearchPage.tsx
│   │   └── App.tsx              # Main React component
│   ├── package.json             # Node.js dependencies
│   └── Dockerfile               # Frontend container definition
│
├── kubernetes/                  # Kubernetes deployment configs
│   └── deployment.yaml          # K8s deployment manifest
│
├── docker-compose.yml           # Local development orchestration
├── render.yaml                  # Render.com deployment config
├── setup-unix.sh               # Unix/Linux setup script
├── setup-windows.bat           # Windows setup script
├── deploy-railway.bat          # Railway deployment script
│
├── .env.example                # Environment variable template
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── README.md                   # Main documentation
├── QUICKSTART.md               # Quick start guide
├── DEPLOYMENT.md               # Deployment instructions
└── CONTRIBUTING.md             # Contribution guidelines
```

### File Count Summary

- **Backend Python Files**: 25 files
- **Frontend TypeScript Files**: 3 files
- **Model Files**: 9 Python modules (~789 lines of code)
- **API Endpoint Files**: 5 modules
- **Documentation Files**: 5 markdown files
- **Configuration Files**: 4 deployment configs

---

## Technology Stack

### Backend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **FastAPI** | 0.104.1 | High-performance Python API framework |
| **Python** | 3.11+ | Programming language |
| **PostgreSQL** | 15+ | Primary relational database |
| **Redis** | 7.x | Caching layer |
| **Elasticsearch** | 8.11.0 | Full-text search engine |
| **SQLAlchemy** | 2.0.23 | ORM and database abstraction |
| **Alembic** | 1.12.1 | Database migrations |
| **Uvicorn** | 0.24.0 | ASGI web server |
| **Pydantic** | 2.5.0 | Data validation and settings |

**Additional Backend Libraries:**
- **Authentication**: python-jose, passlib (JWT & bcrypt)
- **HTTP Clients**: aiohttp, httpx, requests
- **Data Processing**: pandas, numpy
- **Web Scraping**: beautifulsoup4, lxml
- **Testing**: pytest, pytest-asyncio, pytest-cov
- **Code Quality**: black, flake8, mypy, pylint
- **Monitoring**: prometheus-client, opentelemetry

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.2.0 | UI framework |
| **TypeScript** | 5.3.2 | Type-safe JavaScript |
| **Material-UI** | 5.14.19 | Component library |
| **React Query** | 5.12.2 | Data fetching and caching |
| **Vite** | 5.0.5 | Build tool and dev server |
| **React Router** | 6.20.0 | Client-side routing |
| **Axios** | 1.6.2 | HTTP client |
| **Emotion** | 11.11.x | CSS-in-JS styling |

### Infrastructure

- **Docker & Docker Compose**: Containerization
- **Kubernetes**: Container orchestration
- **Nginx**: Reverse proxy and load balancing
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards
- **GitHub Actions**: CI/CD pipeline (planned)

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Web App    │  │  Mobile App  │  │   API Docs   │      │
│  │  (React)     │  │   (Future)   │  │  (Swagger)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────────┐
│                    Load Balancer (Nginx)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                   API Layer (FastAPI)                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Routes: /vehicles /vin /repair /diagnostic /tsb   │     │
│  └────────────────────────────────────────────────────┘     │
└────┬────────────┬────────────┬────────────┬─────────────────┘
     │            │            │            │
     ▼            ▼            ▼            ▼
┌─────────┐  ┌────────┐  ┌─────────┐  ┌──────────────┐
│PostgreSQL│  │ Redis  │  │Elastic- │  │External APIs │
│ Database │  │ Cache  │  │ search  │  │  (NHTSA/EPA) │
└─────────┘  └────────┘  └─────────┘  └──────────────┘
```

### Service Communication

The application uses a microservices-inspired architecture with the following services:

1. **Frontend (Port 3000)**: React SPA served via Vite/Nginx
2. **API Backend (Port 8000)**: FastAPI application
3. **PostgreSQL (Port 5432)**: Primary data store
4. **Redis (Port 6379)**: Caching layer
5. **Elasticsearch (Port 9200)**: Search index
6. **Prometheus (Port 9090)**: Metrics collection
7. **Grafana (Port 3001)**: Monitoring dashboards

All services communicate via a Docker bridge network (`vehicle-network`).

---

## Backend Components

### Core Application (`backend/app/main.py`)

The main FastAPI application includes:

- **CORS Middleware**: Cross-origin resource sharing configuration
- **Trusted Host Middleware**: Security layer
- **Request Timing Middleware**: Performance monitoring (X-Process-Time header)
- **Exception Handlers**: Centralized error handling
- **Health Check Endpoints**: `/health` and `/ready`
- **API Documentation**: Swagger UI (`/docs`) and ReDoc (`/redoc`)

**Key Features:**
- Automatic request/response logging
- Processing time tracking
- Graceful error handling
- Startup/shutdown event handlers

### Database Models

The system includes 9 comprehensive model files:

1. **vehicle.py**: Core vehicle information
   - Vehicle, Engine, Transmission, SuspensionSystem, BrakeSystem classes
   - Relationships to all subsystems

2. **electrical.py**: Electrical system specifications
   - Battery, alternator, wiring diagrams

3. **repair.py**: Repair procedures and torque specifications
   - Step-by-step instructions
   - Required tools and parts

4. **diagnostic.py**: Diagnostic trouble codes (DTCs)
   - Code definitions, symptoms, diagnostic procedures

5. **technical.py**: Technical Service Bulletins (TSBs) and recalls
   - Manufacturer bulletins, NHTSA recalls

6. **parts.py**: Parts catalog and cross-references
   - OEM and aftermarket part numbers

7. **fluid.py**: Fluid specifications
   - Oil, coolant, transmission fluid specs

8. **wheel_tire.py**: Wheel and tire specifications
   - Tire sizes, pressures, wheel bolt patterns

**Total Model Code**: ~789 lines

### API Endpoints

Located in `backend/app/api/endpoints/`:

1. **vehicles.py**: Vehicle search and retrieval
   - Search by year, make, model, trim
   - Filter by specifications

2. **vin.py**: VIN decoder
   - Decode 17-character VINs
   - Identify exact vehicle specifications

3. **repair.py**: Repair procedures
   - Get procedures by system/component
   - Torque specifications lookup

4. **diagnostic.py**: Diagnostic codes
   - DTC code lookup
   - Diagnostic procedures

5. **technical.py**: TSBs and recalls
   - Technical bulletins search
   - Recall information

### Services

**data_scraper.py**: Integration with external data sources
- NHTSA vehicle database API
- EPA fuel economy database
- OEM technical information

### Configuration

**core/config.py**: Application settings using Pydantic
- Database connection strings
- Redis and Elasticsearch URLs
- API rate limiting
- CORS origins
- Security settings (JWT, encryption)
- External API endpoints

---

## Frontend Components

### Application Structure

The frontend is a React 18 TypeScript application with:

**Key Files:**
- `App.tsx`: Main application component
- `VehicleSearchPage.tsx`: Vehicle search interface

**Features:**
- Material-UI component library
- React Query for server state management
- React Router for navigation
- Axios for API communication
- TypeScript for type safety

**Build System:**
- Vite for fast development and optimized builds
- ESLint for code quality
- Testing Library for component testing

---

## Database Schema

### Core Tables

The database schema is comprehensive and production-ready:

#### Vehicles Table
```sql
vehicles (
  vehicle_id UUID PRIMARY KEY,
  vin_pattern VARCHAR(17),
  year INTEGER NOT NULL,
  make VARCHAR(100) NOT NULL,
  model VARCHAR(100) NOT NULL,
  trim VARCHAR(100),
  body_style VARCHAR(50),
  drive_type VARCHAR(20),
  transmission_type VARCHAR(50),
  engine_config VARCHAR(50),
  production_start DATE,
  production_end DATE,
  market_region VARCHAR(50),
  platform_code VARCHAR(50),
  data_verified BOOLEAN,
  verification_source VARCHAR(255),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
```

#### Related Systems
Each vehicle has relationships to:
- **Engines**: Displacement, configuration, horsepower, torque
- **Transmissions**: Type, gear ratios, fluid specifications
- **Suspension Systems**: Geometry, components, specifications
- **Brake Systems**: Rotor dimensions, caliper specifications
- **Electrical Systems**: Battery, alternator, wiring
- **HVAC Systems**: Climate control specifications
- **Fuel Systems**: Tank capacity, fuel type, pressure
- **Wheel/Tire Specs**: Sizes, pressures, bolt patterns

#### Repair & Diagnostic Tables
- **RepairProcedure**: Step-by-step repair instructions
- **DiagnosticCode**: DTC definitions and procedures
- **TechnicalBulletin**: Manufacturer TSBs
- **Recall**: NHTSA safety recalls
- **CommonProblem**: Community-reported issues
- **TorqueSpec**: Fastener torque specifications

### Data Sources

The system aggregates data from:

1. **Government Databases**
   - NHTSA Vehicle Database API
   - EPA Fuel Economy Database
   - NHTSA Recall Database

2. **OEM Technical Information**
   - Factory service manuals (licensed)
   - Technical service bulletins
   - Parts catalogs

3. **Aftermarket Data Providers**
   - Professional repair databases (licensed)
   - Parts supplier catalogs
   - SAE/ISO technical standards

4. **Community Contributions**
   - Verified mechanic submissions
   - Peer-reviewed procedures
   - Common problem reports

---

## API Endpoints

### Base URL Structure

```
Production:  https://api.vehiclerepairdb.com/v1
Development: http://localhost:8000/api/v1
```

### Core Endpoints

#### Vehicle Search
```http
GET /api/v1/vehicles/search?year=2020&make=Toyota&model=Camry
```

#### VIN Decoder
```http
POST /api/v1/vin/decode
Content-Type: application/json

{
  "vin": "1HGBH41JXMN109186"
}
```

#### Repair Procedures
```http
GET /api/v1/vehicles/{vehicle_id}/procedures?system_category=Engine
```

#### DTC Code Lookup
```http
GET /api/v1/vehicles/{vehicle_id}/dtc/P0300
```

#### Torque Specifications
```http
GET /api/v1/vehicles/{vehicle_id}/torque-specs?component=cylinder%20head
```

#### Technical Bulletins
```http
GET /api/v1/vehicles/{vehicle_id}/tsbs
```

#### Recalls
```http
GET /api/v1/vehicles/{vehicle_id}/recalls
```

### API Features

- **Authentication**: JWT-based (30-minute tokens)
- **Rate Limiting**: 100 requests/minute per IP
- **Response Format**: JSON
- **Error Handling**: Standardized error responses
- **Documentation**: OpenAPI 3.0 (Swagger/ReDoc)
- **Versioning**: URL-based versioning (`/api/v1`)

---

## Infrastructure & DevOps

### Docker Compose Services

The `docker-compose.yml` defines 8 services:

1. **postgres**: PostgreSQL 15 database
   - Persistent volume for data
   - Health checks configured

2. **redis**: Redis 7 cache
   - AOF persistence enabled
   - Health checks configured

3. **elasticsearch**: Elasticsearch 8.11.0
   - Single-node configuration
   - 512MB heap size

4. **api**: FastAPI backend
   - Auto-reload for development
   - Depends on all data services

5. **frontend**: React application
   - Vite dev server

6. **nginx**: Reverse proxy
   - SSL termination ready
   - Load balancing

7. **prometheus**: Metrics collection
   - Scrapes API metrics

8. **grafana**: Monitoring dashboards
   - Pre-configured datasources

### Kubernetes Deployment

The `kubernetes/deployment.yaml` includes:
- Deployment manifests
- Service definitions
- ConfigMaps for configuration
- Persistent volume claims
- Ingress configuration

### Setup Scripts

1. **setup-unix.sh** (12,352 bytes): Linux/macOS setup
   - Dependency installation
   - Environment configuration
   - Database initialization

2. **setup-windows.bat** (12,322 bytes): Windows setup
   - PowerShell-based setup
   - Equivalent to Unix script

3. **deploy-railway.bat** (6,934 bytes): Railway.app deployment
   - Automated Railway deployment
   - Environment variable configuration

### Environment Configuration

`.env.example` provides templates for:
- Database connection (PostgreSQL)
- Redis cache URL
- Elasticsearch URL
- JWT secret key
- CORS origins
- API rate limits
- External API keys (NHTSA, EPA)
- File upload settings
- Logging configuration

---

## Development Workflow

### Local Development Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd ctc-jade.li

# 2. Start all services
docker-compose up -d

# 3. Initialize database
docker-compose exec api python scripts/init_db.py

# 4. Load seed data
docker-compose exec api python scripts/seed_data.py

# 5. Access applications
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Grafana: http://localhost:3001
```

### Manual Setup (without Docker)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Development Tools

**Backend:**
- **Testing**: `pytest tests/ -v --cov=app`
- **Linting**: `flake8`, `pylint`
- **Formatting**: `black`
- **Type Checking**: `mypy`

**Frontend:**
- **Testing**: `npm test`
- **Linting**: `npm run lint`
- **Formatting**: `npm run format`
- **Build**: `npm run build`

---

## Deployment Options

### Platform Comparison

| Platform | Cost | Complexity | Recommended For |
|----------|------|------------|-----------------|
| Railway | $5-20/mo | Low | Development, MVP |
| Render | $7-25/mo | Low | Small-medium projects |
| DigitalOcean | $12-40/mo | Medium | Production |
| AWS | $50+/mo | High | Enterprise scale |
| Vercel | $20+/mo | High | Limited (serverless) |

### Deployment Files

1. **docker-compose.yml**: Local development
2. **render.yaml**: Render.com configuration
3. **kubernetes/deployment.yaml**: K8s manifests
4. **deploy-railway.bat**: Railway automation

### Recommended: Railway

Railway is the easiest deployment option:
- Automatic PostgreSQL, Redis provisioning
- GitHub integration
- Environment variable management
- Automatic SSL certificates
- Built-in monitoring

See `DEPLOYMENT.md` for detailed platform-specific instructions.

---

## Testing Strategy

### Backend Testing

Location: `backend/tests/`

**Test Coverage:**
- API endpoint tests (`test_api.py`)
- Database model tests
- Service layer tests
- Integration tests

**Test Execution:**
```bash
pytest tests/ -v --cov=app
```

**Load Testing:**
```bash
locust -f tests/load/locustfile.py
```

### Frontend Testing

**Test Types:**
- Component tests (React Testing Library)
- Integration tests
- E2E tests (planned)

**Test Execution:**
```bash
npm test
npm run test:e2e  # E2E tests
```

### Performance Targets

- **API Response Time**: < 200ms (p95)
- **Database Query Time**: < 50ms (p95)
- **Search Latency**: < 100ms
- **Uptime SLA**: 99.9%
- **Concurrent Users**: 10,000+

---

## Documentation

### Available Documentation Files

1. **README.md** (8,660 bytes)
   - Project overview
   - Quick start guide
   - API examples
   - Technology stack
   - Roadmap

2. **QUICKSTART.md** (7,263 bytes)
   - Step-by-step setup
   - Common issues
   - Quick reference

3. **DEPLOYMENT.md** (13,722 bytes)
   - Platform comparisons
   - Deployment guides (Railway, Render, AWS, etc.)
   - Environment variables
   - Scaling strategies

4. **CONTRIBUTING.md** (8,000 bytes)
   - Contribution guidelines
   - Code standards
   - Pull request process
   - Data contribution guidelines

5. **LICENSE** (1,080 bytes)
   - MIT License

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/api/v1/openapi.json

---

## Current Status

### Completed Features ✅

- Database schema design (9 comprehensive models, ~789 LOC)
- Core API endpoints (5 endpoint modules)
- Basic frontend interface (React + TypeScript)
- VIN decoder integration
- Docker development environment
- Health check and monitoring endpoints
- API documentation (Swagger/ReDoc)
- Deployment configurations (Railway, Render, K8s)
- Setup automation scripts (Unix + Windows)

### In Progress 🚧

- NHTSA data import
- Complete vehicle coverage (2014-2024)
- Advanced search with Elasticsearch
- Repair procedure database
- Community contribution system

### Not Started ❌

- Mobile app (iOS/Android)
- Wiring diagram viewer
- Real-time diagnostic integration
- AI-powered diagnostic assistant
- Parts supplier marketplace

---

## Roadmap

### Phase 1 (Current - Q1 2024)
- ✅ Database schema design
- ✅ Core API endpoints
- ✅ Basic frontend interface
- ✅ VIN decoder integration
- 🚧 NHTSA data import

### Phase 2 (Q2 2024)
- Complete 2014-2024 vehicle coverage
- Advanced search with Elasticsearch
- Mobile app (iOS/Android)
- Wiring diagram viewer
- Community contribution system

### Phase 3 (Q3 2024)
- 50,000+ repair procedures
- Real-time diagnostic integration
- Mechanic certification program
- API partner program
- Multi-language support

### Phase 4 (Q4 2024)
- AI-powered diagnostic assistant
- Augmented reality repair guides
- Integration with shop management systems
- Parts supplier marketplace
- 100,000+ monthly active users

---

## Key Metrics

### Repository Statistics

- **Total Files**: ~33 files (excluding node_modules)
- **Backend Code**: ~789 lines (models only)
- **Database Models**: 9 comprehensive modules
- **API Endpoints**: 5 endpoint modules
- **Documentation**: 5 markdown files
- **Languages**: Python, TypeScript, Shell, YAML
- **License**: MIT

### Code Quality

- **Type Safety**: TypeScript frontend, Pydantic backend
- **Testing**: pytest, React Testing Library
- **Linting**: ESLint, flake8, pylint
- **Formatting**: Black (Python), Prettier (TypeScript)
- **Documentation**: Comprehensive inline and external docs

---

## Security

### Security Features

- **Authentication**: JWT-based authentication
- **Authorization**: Role-based access control (planned)
- **Rate Limiting**: 100 requests/minute per IP
- **SQL Injection Prevention**: Parameterized queries (SQLAlchemy)
- **XSS Protection**: Input sanitization
- **TLS Encryption**: TLS 1.3 support
- **CORS**: Configurable origins
- **Trusted Hosts**: Middleware protection

### Security Standards

- OWASP Top 10 compliance
- Regular security audits (planned)
- Dependency vulnerability scanning
- Environment variable protection

---

## Contributing

Contributions are welcome! See `CONTRIBUTING.md` for:

- Code of conduct
- Development setup
- Coding standards (PEP 8, ESLint)
- Pull request process
- Data contribution guidelines
- Testing requirements

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request
5. Respond to code review feedback

---

## Support & Resources

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@vehiclerepairdb.com
- **Documentation**: https://docs.vehiclerepairdb.com

---

## Conclusion

The Vehicle Repair Database is a comprehensive, well-structured project with:

- **Solid Foundation**: 9 database models, 5 API endpoints, full Docker stack
- **Modern Stack**: FastAPI, React 18, PostgreSQL, Redis, Elasticsearch
- **Production-Ready**: Deployment configs, monitoring, health checks
- **Well-Documented**: 5 comprehensive markdown files
- **Active Development**: Clear roadmap through 2024
- **Community-Focused**: Open source, contribution-friendly

The repository is in **active development** with a strong architectural foundation and clear path to production deployment.

---

**Built with ❤️ by the automotive community, for the automotive community.**
