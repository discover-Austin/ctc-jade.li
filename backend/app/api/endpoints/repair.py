"""
Repair procedures and maintenance API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.base import get_db
from app.models.repair import RepairProcedure, TorqueSpec, MaintenanceSchedule
from app.schemas.repair import (
    RepairProcedureResponse,
    TorqueSpecResponse,
    MaintenanceScheduleResponse
)

router = APIRouter()


@router.get("/procedures/{vehicle_id}", response_model=List[RepairProcedureResponse])
async def get_repair_procedures(
    vehicle_id: UUID,
    system_category: Optional[str] = Query(None, description="Filter by system (Engine, Transmission, etc.)"),
    difficulty_level: Optional[str] = Query(None, description="Filter by difficulty level"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Retrieve all repair procedures for a specific vehicle.

    Optional filters:
    - **system_category**: Filter by system (Engine, Transmission, Brakes, etc.)
    - **difficulty_level**: Filter by difficulty (Beginner, Intermediate, Advanced, Professional)
    - **limit**: Maximum number of results
    - **offset**: Number of results to skip

    Returns detailed step-by-step repair procedures with:
    - Required tools and parts
    - Torque specifications
    - Safety precautions
    - Photos and videos
    - Common mistakes and tips
    """
    query = db.query(RepairProcedure).filter(RepairProcedure.vehicle_id == vehicle_id)

    if system_category:
        query = query.filter(RepairProcedure.system_category.ilike(f"%{system_category}%"))

    if difficulty_level:
        query = query.filter(RepairProcedure.difficulty_level == difficulty_level)

    procedures = query.offset(offset).limit(limit).all()

    return procedures


@router.get("/procedures/detail/{procedure_id}", response_model=RepairProcedureResponse)
async def get_repair_procedure_detail(
    procedure_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get detailed information for a specific repair procedure.

    Returns complete procedure including:
    - Step-by-step instructions
    - Torque specifications with sequences
    - Required tools and parts
    - Clearance and wear limits
    - Photos and videos
    - Technical notes and tips
    - Related DTC codes and TSBs
    """
    procedure = db.query(RepairProcedure).filter(
        RepairProcedure.procedure_id == procedure_id
    ).first()

    if not procedure:
        raise HTTPException(status_code=404, detail="Repair procedure not found")

    return procedure


@router.get("/torque-specs/{vehicle_id}", response_model=List[TorqueSpecResponse])
async def get_torque_specifications(
    vehicle_id: UUID,
    component: Optional[str] = Query(None, description="Filter by component name"),
    system_category: Optional[str] = Query(None, description="Filter by system category"),
    db: Session = Depends(get_db)
):
    """
    Retrieve torque specifications for vehicle components.

    Optional filters:
    - **component**: Search for specific component (e.g., "cylinder head", "wheel lug")
    - **system_category**: Filter by system (Engine, Transmission, Chassis, etc.)

    Returns comprehensive torque specifications including:
    - Component name and description
    - Torque values in lb-ft and Nm
    - Tightening sequence and pattern
    - Thread locker requirements
    - Lubrication requirements
    - Bolt reusability information
    """
    query = db.query(TorqueSpec).filter(TorqueSpec.vehicle_id == vehicle_id)

    if component:
        query = query.filter(TorqueSpec.component_name.ilike(f"%{component}%"))

    if system_category:
        query = query.filter(TorqueSpec.system_category == system_category)

    specs = query.all()

    if not specs:
        raise HTTPException(status_code=404, detail="No torque specifications found")

    return specs


@router.get("/maintenance/{vehicle_id}", response_model=List[MaintenanceScheduleResponse])
async def get_maintenance_schedule(
    vehicle_id: UUID,
    mileage: Optional[int] = Query(None, description="Current vehicle mileage"),
    interval_type: Optional[str] = Query(None, description="Normal or Severe conditions"),
    db: Session = Depends(get_db)
):
    """
    Retrieve maintenance schedule for a vehicle.

    Optional filters:
    - **mileage**: Show services due within next 5000 miles of current mileage
    - **interval_type**: Filter by Normal or Severe driving conditions

    Returns OEM-recommended maintenance schedule including:
    - Service intervals (miles and months)
    - Required parts and fluids
    - Estimated cost range
    - Priority level
    - Inspection points
    """
    query = db.query(MaintenanceSchedule).filter(
        MaintenanceSchedule.vehicle_id == vehicle_id
    )

    if interval_type:
        query = query.filter(MaintenanceSchedule.interval_type == interval_type)

    if mileage:
        # Return services due within next 5000 miles
        query = query.filter(
            MaintenanceSchedule.interval_miles <= mileage + 5000,
            MaintenanceSchedule.interval_miles >= mileage
        )

    schedules = query.order_by(MaintenanceSchedule.interval_miles).all()

    return schedules


@router.get("/systems")
async def get_system_categories():
    """
    Get list of all available system categories for repair procedures.

    Returns:
    - List of system categories (Engine, Transmission, Brakes, Electrical, etc.)
    - Count of procedures per category
    """
    return {
        "categories": [
            "Engine",
            "Transmission",
            "Brakes",
            "Suspension",
            "Steering",
            "Electrical",
            "HVAC",
            "Fuel System",
            "Exhaust",
            "Cooling System",
            "Body",
            "Interior",
            "Wheels and Tires"
        ]
    }


@router.get("/difficulty-levels")
async def get_difficulty_levels():
    """
    Get list of all repair procedure difficulty levels.

    Returns:
    - Beginner: Basic maintenance, simple repairs
    - Intermediate: Moderate mechanical skill required
    - Advanced: Significant experience and tools needed
    - Professional: Dealer/shop level repair, special equipment required
    """
    return {
        "levels": [
            {
                "level": "Beginner",
                "description": "Basic maintenance and simple repairs. Minimal tools required.",
                "examples": ["Oil change", "Air filter replacement", "Wiper blade installation"]
            },
            {
                "level": "Intermediate",
                "description": "Moderate mechanical skill required. Standard tools needed.",
                "examples": ["Brake pad replacement", "Spark plug replacement", "Alternator replacement"]
            },
            {
                "level": "Advanced",
                "description": "Significant experience and specialized tools needed.",
                "examples": ["Timing belt replacement", "Head gasket repair", "Transmission service"]
            },
            {
                "level": "Professional",
                "description": "Dealer/shop level repair. Special equipment and training required.",
                "examples": ["Engine rebuild", "Transmission rebuild", "ECU programming"]
            }
        ]
    }
