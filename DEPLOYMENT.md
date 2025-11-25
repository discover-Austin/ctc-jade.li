# Deployment Guide - Vehicle Repair Database

This guide covers deploying the Vehicle Repair Database to various hosting platforms.

## Table of Contents

- [Platform Comparison](#platform-comparison)
- [Railway Deployment](#railway-deployment-recommended)
- [Render Deployment](#render-deployment)
- [DigitalOcean App Platform](#digitalocean-app-platform)
- [Vercel Deployment](#vercel-deployment-limited)
- [AWS Deployment](#aws-deployment-production)
- [Environment Variables](#environment-variables)

---

## Platform Comparison

| Platform | Backend | Database | Redis | Elasticsearch | Cost | Complexity | Recommended |
|----------|---------|----------|-------|---------------|------|------------|-------------|
| **Railway** | ✅ | ✅ PostgreSQL | ✅ | ✅ | $5-20/mo | Low | ⭐⭐⭐⭐⭐ |
| **Render** | ✅ | ✅ PostgreSQL | ✅ | ❌ | $7-25/mo | Low | ⭐⭐⭐⭐ |
| **DigitalOcean** | ✅ | ✅ Managed DB | ✅ | ✅ | $12-40/mo | Medium | ⭐⭐⭐⭐ |
| **Vercel** | ⚠️ Serverless | ❌ (Vercel Postgres) | ❌ | ❌ | $20+/mo | High | ⭐⭐ |
| **AWS** | ✅ | ✅ RDS | ✅ ElastiCache | ✅ | $50+/mo | High | ⭐⭐⭐⭐⭐ |

**Recommendation**: **Railway** for easiest deployment, **AWS/DigitalOcean** for production scale.

---

## Railway Deployment (RECOMMENDED)

Railway is the **easiest and most cost-effective** option for this full-stack application.

### Prerequisites
- Railway account (free tier available)
- GitHub repository

### Steps

#### 1. Create Railway Project

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init
```

#### 2. Add Services

```bash
# Add PostgreSQL database
railway add --database postgres

# Add Redis cache
railway add --database redis

# Add Elasticsearch (optional, requires plugin)
# Note: Use managed Elasticsearch service if needed
```

#### 3. Deploy Backend

Create `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "backend/Dockerfile"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### 4. Configure Environment Variables

In Railway dashboard, add:

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
SECRET_KEY=<generate-secure-key>
BACKEND_CORS_ORIGINS=https://your-frontend.railway.app
```

#### 5. Deploy

```bash
# Deploy backend
railway up

# Get deployment URL
railway domain
```

#### 6. Deploy Frontend

Create separate Railway service:

```bash
# In frontend directory
railway init

# Add build settings
railway add
```

Add `frontend/railway.json`:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "npm run preview"
  }
}
```

Environment variables:
```env
VITE_API_URL=https://your-backend.railway.app/api/v1
```

### Estimated Cost
- **Free Tier**: $5 credit/month (good for development)
- **Hobby**: $5/month per service
- **Production**: ~$15-20/month total

---

## Render Deployment

Render offers a simple deployment with great developer experience.

### Steps

#### 1. Create Blueprint File

Create `render.yaml`:

```yaml
services:
  # Backend API
  - type: web
    name: vehicle-db-api
    env: python
    region: oregon
    buildCommand: pip install -r backend/requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: vehicle-db-postgres
          property: connectionString
      - key: REDIS_URL
        fromDatabase:
          name: vehicle-db-redis
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.11.0

  # Frontend
  - type: web
    name: vehicle-db-frontend
    env: node
    region: oregon
    buildCommand: cd frontend && npm install && npm run build
    startCommand: cd frontend && npm run preview
    envVars:
      - key: VITE_API_URL
        value: https://vehicle-db-api.onrender.com/api/v1

databases:
  # PostgreSQL
  - name: vehicle-db-postgres
    databaseName: vehicle_db
    user: vehicle_user
    region: oregon
    plan: starter

  # Redis
  - name: vehicle-db-redis
    region: oregon
    plan: starter
```

#### 2. Deploy

1. Connect GitHub repository to Render
2. Render will auto-detect `render.yaml`
3. Click "Apply" to deploy all services

#### 3. Run Migrations

```bash
# SSH into the API service
render ssh vehicle-db-api

# Run migrations
cd backend
alembic upgrade head
```

### Estimated Cost
- **Free Tier**: Limited (apps spin down after 15min inactivity)
- **Starter**: $7/month per service
- **Production**: ~$25/month total

---

## DigitalOcean App Platform

Best for production deployments with predictable scaling.

### Steps

#### 1. Create App Spec

Create `.do/app.yaml`:

```yaml
name: vehicle-repair-database
region: nyc

services:
  # Backend API
  - name: api
    source:
      repo: your-username/vehicle-db
      branch: main
    dockerfile_path: backend/Dockerfile
    http_port: 8000
    instance_count: 2
    instance_size_slug: professional-xs
    health_check:
      http_path: /health
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        value: ${db.DATABASE_URL}
      - key: REDIS_URL
        scope: RUN_TIME
        value: ${redis.REDIS_URL}
      - key: SECRET_KEY
        scope: RUN_TIME
        type: SECRET
        value: YOUR_SECRET_KEY

  # Frontend
  - name: frontend
    source:
      repo: your-username/vehicle-db
      branch: main
    build_command: cd frontend && npm install && npm run build
    run_command: cd frontend && npm run preview
    http_port: 3000
    instance_count: 1
    instance_size_slug: basic-xs
    envs:
      - key: VITE_API_URL
        value: ${api.PUBLIC_URL}/api/v1

databases:
  - name: db
    engine: PG
    version: "15"
    production: true
    cluster_name: vehicle-db-cluster

  - name: redis
    engine: REDIS
    version: "7"
```

#### 2. Deploy

```bash
# Install doctl CLI
brew install doctl  # macOS
# or download from https://docs.digitalocean.com/reference/doctl/

# Authenticate
doctl auth init

# Create app
doctl apps create --spec .do/app.yaml

# Or use the web interface
# https://cloud.digitalocean.com/apps
```

### Estimated Cost
- **Basic**: $12/month (1 service + database)
- **Professional**: $40+/month (multiple services, managed DB)

---

## Vercel Deployment (LIMITED)

⚠️ **Important**: Vercel is **NOT recommended** for this application because:
- No support for long-running processes (PostgreSQL, Redis)
- Serverless functions have 10-60s timeout limits
- Requires significant code refactoring
- Higher cost for databases (Vercel Postgres, Upstash Redis)

### If You Must Use Vercel

#### Required Changes

1. **Convert Backend to Serverless Functions**

Create `api/index.py` (Vercel serverless handler):

```python
from fastapi import FastAPI
from mangum import Mangum
from app.main import app

# Wrap FastAPI for serverless
handler = Mangum(app)
```

2. **Use Vercel Postgres**

```bash
# Install Vercel CLI
npm install -g vercel

# Add Postgres
vercel postgres create
```

3. **Use Upstash Redis**

Sign up at https://upstash.com and get Redis URL

4. **Modify Database Connections**

Update `backend/app/db/base.py`:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

# Serverless-friendly connection
DATABASE_URL = os.getenv("POSTGRES_URL")
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # No connection pooling for serverless
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=60000"
    }
)
```

5. **Create `vercel.json`**

```json
{
  "buildCommand": "cd backend && pip install -r requirements.txt",
  "devCommand": "cd backend && uvicorn app.main:app --reload",
  "installCommand": "pip install -r backend/requirements.txt",
  "framework": null,
  "outputDirectory": "frontend/dist",
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "/api/index.py"
    }
  ],
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.11",
      "maxDuration": 60
    }
  },
  "env": {
    "POSTGRES_URL": "@postgres_url",
    "REDIS_URL": "@redis_url",
    "SECRET_KEY": "@secret_key"
  }
}
```

6. **Deploy**

```bash
# Deploy
vercel

# Add environment variables
vercel env add POSTGRES_URL
vercel env add REDIS_URL
vercel env add SECRET_KEY

# Production deployment
vercel --prod
```

### Limitations on Vercel
- ❌ No Elasticsearch support
- ❌ 60-second timeout on API routes
- ❌ Cold starts (slower initial requests)
- ❌ No background jobs/data scraping
- ❌ Limited database connections
- 💰 Higher cost (~$20+/month for Postgres + Redis)

### Estimated Cost
- **Hobby**: $20/month (Vercel Pro required)
- **With Database**: $40+/month (Vercel Postgres + Upstash Redis)

---

## AWS Deployment (Production Scale)

For high-traffic production deployment.

### Architecture
- **ECS Fargate**: Docker containers
- **RDS PostgreSQL**: Managed database
- **ElastiCache Redis**: Managed cache
- **OpenSearch**: Managed Elasticsearch
- **CloudFront**: CDN
- **Route 53**: DNS
- **ALB**: Load balancing

### Quick Deploy with CDK

Create `aws-cdk/app.py`:

```python
from aws_cdk import (
    Stack, App,
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_ecs as ecs,
    aws_elasticache as elasticache,
)

class VehicleDbStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "VehicleDbVpc", max_azs=2)

        # RDS PostgreSQL
        db = rds.DatabaseInstance(
            self, "Database",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_15),
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.T3, ec2.InstanceSize.MICRO),
            vpc=vpc,
            multi_az=True,
            allocated_storage=20,
            database_name="vehicle_db"
        )

        # ECS Cluster
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        # Task Definition
        task_def = ecs.FargateTaskDefinition(self, "TaskDef")

        container = task_def.add_container(
            "api",
            image=ecs.ContainerImage.from_asset("./backend"),
            environment={
                "DATABASE_URL": db.instance_endpoint.socket_address
            },
            logging=ecs.LogDrivers.aws_logs(stream_prefix="vehicle-db")
        )

        container.add_port_mappings(ecs.PortMapping(container_port=8000))

        # Service
        ecs.FargateService(
            self, "Service",
            cluster=cluster,
            task_definition=task_def,
            desired_count=2
        )

app = App()
VehicleDbStack(app, "VehicleDbStack")
app.synth()
```

Deploy:

```bash
# Install AWS CDK
npm install -g aws-cdk

# Bootstrap
cdk bootstrap

# Deploy
cdk deploy
```

### Estimated Cost
- **Development**: $50-100/month
- **Production**: $200-500/month (depending on traffic)

---

## Environment Variables

All platforms require these environment variables:

### Required

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/vehicle_db

# Redis Cache
REDIS_URL=redis://host:6379/0

# Security
SECRET_KEY=<generate-strong-random-key>

# CORS
BACKEND_CORS_ORIGINS=https://your-frontend-domain.com
```

### Optional

```env
# Elasticsearch
ELASTICSEARCH_URL=http://elasticsearch:9200

# API Configuration
API_V1_STR=/api/v1
RATE_LIMIT_PER_MINUTE=100

# External APIs
NHTSA_API_BASE_URL=https://vpic.nhtsa.dot.gov/api
EPA_API_BASE_URL=https://www.fueleconomy.gov/feg

# Logging
LOG_LEVEL=INFO
```

### Generate SECRET_KEY

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32
```

---

## Post-Deployment

### 1. Run Database Migrations

```bash
# Railway/Render
railway run alembic upgrade head

# Or SSH into container
alembic upgrade head
```

### 2. Populate Database

```bash
# Run data import script
python scripts/import_nhtsa_data.py
```

### 3. Health Check

```bash
# Check API health
curl https://your-api-url.com/health

# Check database connection
curl https://your-api-url.com/ready
```

### 4. Monitor

- Set up logging aggregation
- Configure alerts for errors
- Monitor database performance
- Track API response times

---

## Troubleshooting

### Database Connection Issues

```python
# Test connection
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    result = conn.execute("SELECT 1")
    print(result.fetchone())
```

### CORS Errors

Update `backend/app/core/config.py`:

```python
BACKEND_CORS_ORIGINS = [
    "https://your-frontend.vercel.app",
    "https://your-frontend.railway.app",
    "http://localhost:3000"
]
```

### Slow Queries

```sql
-- Enable slow query logging
ALTER DATABASE vehicle_db SET log_min_duration_statement = 1000;

-- Check slow queries
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

---

## Recommendation Summary

**For Quick Testing**: Use **Railway** (easiest, cheapest)
**For Production**: Use **DigitalOcean** or **AWS** (scalable, reliable)
**Avoid**: **Vercel** (requires major refactoring, not designed for this architecture)

---

## Support

For deployment issues:
- Check platform-specific documentation
- Review application logs
- Test locally with Docker first
- Contact platform support if needed
