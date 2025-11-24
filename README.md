# Vehicle Repair Database & Guide System

A comprehensive, production-grade vehicle database and repair guide system for 2014+ vehicles. This platform provides factory-level repair information, technical specifications, diagnostic procedures, and maintenance schedules for mechanics, technicians, and DIY enthusiasts.

## 🎯 Mission Statement

Build a comprehensive, free-to-access vehicle repair database that empowers mechanics, technicians, and DIY enthusiasts with factory-level information for all vehicles manufactured from 2014 onwards.

## ✨ Key Features

- **Comprehensive Vehicle Database**: Detailed specifications for 2014+ vehicles
- **Repair Procedures**: Step-by-step instructions with torque specifications
- **DTC Code Database**: Diagnostic trouble codes with diagnostic procedures
- **Technical Service Bulletins**: Manufacturer TSBs and recall information
- **Wiring Diagrams**: Electrical schematics and connector locations
- **Maintenance Schedules**: OEM-recommended service intervals
- **VIN Decoder**: Decode VINs to identify exact vehicle specifications
- **Parts Cross-Reference**: OEM and aftermarket part interchanges
- **Common Problems Database**: Community-reported issues and solutions

## 🏗️ Architecture

### Backend Stack
- **FastAPI**: High-performance Python API framework
- **PostgreSQL**: Primary relational database
- **Redis**: Caching layer
- **Elasticsearch**: Full-text search engine
- **SQLAlchemy**: ORM and database migrations

### Frontend Stack
- **React 18**: Modern UI framework
- **TypeScript**: Type-safe development
- **Material-UI**: Component library
- **React Query**: Data fetching and caching
- **Vite**: Build tool and dev server

### Infrastructure
- **Docker**: Containerization
- **Kubernetes**: Orchestration
- **Nginx**: Reverse proxy and load balancing
- **Prometheus/Grafana**: Monitoring and metrics
- **GitHub Actions**: CI/CD pipeline

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd ctc-jade.li

# Start all services with Docker Compose
docker-compose up -d

# Initialize the database
docker-compose exec api python scripts/init_db.py

# Load seed data
docker-compose exec api python scripts/seed_data.py

# Access the application
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Manual Setup

```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the API server
uvicorn app.main:app --reload

# Frontend setup (in a new terminal)
cd frontend
npm install
npm run dev
```

## 📊 Database Schema

The system uses a comprehensive relational database schema covering:

- **Vehicles**: Make, model, year, trim, platform codes
- **Engines**: Displacement, configuration, specifications
- **Transmissions**: Type, gear ratios, fluid specifications
- **Suspension & Chassis**: Geometry, components, specifications
- **Brake Systems**: Rotor dimensions, caliper specifications
- **Electrical Systems**: Battery, alternator, wiring diagrams
- **Repair Procedures**: Step-by-step instructions with torque specs
- **Diagnostic Codes**: DTC definitions and diagnostic procedures
- **Technical Bulletins**: Manufacturer TSBs and service campaigns
- **Recalls**: NHTSA safety recalls and remedies

## 🔌 API Documentation

### Base URL
```
Production: https://api.vehiclerepairdb.com/v1
Development: http://localhost:8000/api/v1
```

### Key Endpoints

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

Full API documentation available at `/docs` (Swagger UI) and `/redoc` (ReDoc).

## 🗃️ Data Sources

This system aggregates data from multiple authoritative sources:

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
   - Technical standards organizations (SAE, ISO)

4. **Community Contributions**
   - Verified mechanic submissions
   - Peer-reviewed procedures
   - Common problem reports

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e

# Load testing
cd backend
locust -f tests/load/locustfile.py
```

## 🚢 Deployment

### Docker Deployment
```bash
# Build images
docker-compose build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment
```bash
# Apply configurations
kubectl apply -f kubernetes/

# Check deployment status
kubectl get pods -n vehicle-db
```

## 📈 Performance Targets

- **API Response Time**: < 200ms (p95)
- **Database Query Time**: < 50ms (p95)
- **Search Latency**: < 100ms
- **Uptime SLA**: 99.9%
- **Concurrent Users**: 10,000+

## 🔒 Security

- JWT-based authentication
- API rate limiting (100 req/min per IP)
- SQL injection prevention (parameterized queries)
- XSS protection (input sanitization)
- TLS 1.3 encryption
- Regular security audits
- OWASP Top 10 compliance

## 🤝 Contributing

We welcome contributions from the automotive community!

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow the code style guide (PEP 8 for Python, ESLint for TypeScript)
- Write comprehensive tests for new features
- Update documentation for API changes
- Verify data accuracy before submitting repair procedures
- Include sources for technical specifications

### Data Contribution

Mechanics and technicians can contribute:
- Repair procedures with photos
- Torque specifications
- Common problem reports
- Wiring diagrams
- Diagnostic procedures

All contributions are peer-reviewed by certified mechanics before publication.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- NHTSA for vehicle and recall data
- EPA for fuel economy data
- Contributing mechanics and technicians
- Open source community

## 📞 Contact & Support

- **Documentation**: https://docs.vehiclerepairdb.com
- **Issues**: https://github.com/your-org/vehicle-db/issues
- **Discussions**: https://github.com/your-org/vehicle-db/discussions
- **Email**: support@vehiclerepairdb.com

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ Database schema design
- ✅ Core API endpoints
- ✅ Basic frontend interface
- ✅ VIN decoder integration
- ✅ NHTSA data import

### Phase 2 (Q2 2024)
- [ ] Complete 2014-2024 vehicle coverage
- [ ] Advanced search with Elasticsearch
- [ ] Mobile app (iOS/Android)
- [ ] Wiring diagram viewer
- [ ] Community contribution system

### Phase 3 (Q3 2024)
- [ ] 50,000+ repair procedures
- [ ] Real-time diagnostic integration
- [ ] Mechanic certification program
- [ ] API partner program
- [ ] Multi-language support

### Phase 4 (Q4 2024)
- [ ] AI-powered diagnostic assistant
- [ ] Augmented reality repair guides
- [ ] Integration with shop management systems
- [ ] Parts supplier marketplace
- [ ] 100,000+ monthly active users

## 📊 Project Status

![Build Status](https://img.shields.io/github/workflow/status/your-org/vehicle-db/CI)
![Coverage](https://img.shields.io/codecov/c/github/your-org/vehicle-db)
![License](https://img.shields.io/github/license/your-org/vehicle-db)
![Contributors](https://img.shields.io/github/contributors/your-org/vehicle-db)
![Stars](https://img.shields.io/github/stars/your-org/vehicle-db)

---

**Built with ❤️ by the automotive community, for the automotive community.**
