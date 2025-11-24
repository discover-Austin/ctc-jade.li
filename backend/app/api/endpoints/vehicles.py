"""
Vehicle API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.base import get_db
from app.models.vehicle import Vehicle, Engine, Transmission
from app.schemas.vehicle import (
    VehicleResponse,
    VehicleSearchRequest,
    VehicleDetailResponse,
    EngineResponse,
    TransmissionResponse
)

router = APIRouter()


@router.get("/search", response_model=List[VehicleResponse])
async def search_vehicles(
    year: Optional[int] = Query(None, ge=2014, le=2030),
    make: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    engine: Optional[str] = Query(None),
    vin: Optional[str] = Query(None, min_length=17, max_length=17),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Search for vehicles by year, make, model, engine, or VIN.
    Returns comprehensive vehicle specifications.

    - **year**: Model year (2014-2030)
    - **make**: Vehicle manufacturer
    - **model**: Vehicle model name
    - **engine**: Engine configuration
    - **vin**: Vehicle Identification Number (17 characters)
    - **limit**: Maximum number of results (1-100, default 50)
    - **offset**: Number of results to skip (pagination)
    """
    query = db.query(Vehicle)

    # Apply filters
    if year:
        query = query.filter(Vehicle.year == year)
    if make:
        query = query.filter(Vehicle.make.ilike(f"%{make}%"))
    if model:
        query = query.filter(Vehicle.model.ilike(f"%{model}%"))
    if engine:
        query = query.filter(Vehicle.engine_config.ilike(f"%{engine}%"))
    if vin:
        # VIN search - match by VIN pattern
        query = query.filter(Vehicle.vin_pattern == vin[:11])

    # Apply pagination
    vehicles = query.offset(offset).limit(limit).all()

    if not vehicles:
        raise HTTPException(status_code=404, detail="No vehicles found matching criteria")

    return vehicles


@router.get("/{vehicle_id}", response_model=VehicleDetailResponse)
async def get_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get detailed information for a specific vehicle by ID.

    Returns vehicle specifications along with related engines and transmissions.
    """
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle


@router.get("/{vehicle_id}/engines", response_model=List[EngineResponse])
async def get_vehicle_engines(
    vehicle_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get all engine configurations for a specific vehicle.

    Returns detailed engine specifications including displacement,
    horsepower, torque, and hybrid/electric details.
    """
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    engines = db.query(Engine).filter(Engine.vehicle_id == vehicle_id).all()

    return engines


@router.get("/{vehicle_id}/transmissions", response_model=List[TransmissionResponse])
async def get_vehicle_transmissions(
    vehicle_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get all transmission configurations for a specific vehicle.

    Returns detailed transmission specifications including type,
    speeds, gear ratios, and fluid specifications.
    """
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    transmissions = db.query(Transmission).filter(Transmission.vehicle_id == vehicle_id).all()

    return transmissions


@router.get("/{vehicle_id}/specifications")
async def get_vehicle_specifications(
    vehicle_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get comprehensive specifications for a vehicle including:
    - Engine specifications
    - Transmission specifications
    - Suspension system
    - Brake system
    - Electrical system
    - HVAC system
    - Fuel system
    - Wheel and tire specifications
    """
    vehicle = db.query(Vehicle).filter(Vehicle.vehicle_id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Compile all specifications
    specifications = {
        "vehicle": VehicleResponse.from_orm(vehicle),
        "engines": [EngineResponse.from_orm(e) for e in vehicle.engines],
        "transmissions": [TransmissionResponse.from_orm(t) for t in vehicle.transmissions],
        "suspension_systems": vehicle.suspension_systems,
        "brake_systems": vehicle.brake_systems,
        "electrical_systems": vehicle.electrical_systems,
        "hvac_systems": vehicle.hvac_systems,
        "fuel_systems": vehicle.fuel_systems,
        "wheel_tire_specs": vehicle.wheel_tire_specs,
    }

    return specifications
