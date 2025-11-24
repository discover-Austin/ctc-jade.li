"""
API router configuration.
"""
from fastapi import APIRouter
from app.api.endpoints import vehicles, repair, diagnostic, technical, vin

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["Vehicles"])
api_router.include_router(vin.router, prefix="/vin", tags=["VIN Decoder"])
api_router.include_router(repair.router, prefix="/repair", tags=["Repair"])
api_router.include_router(diagnostic.router, prefix="/diagnostic", tags=["Diagnostic"])
api_router.include_router(technical.router, prefix="/technical", tags=["Technical"])
