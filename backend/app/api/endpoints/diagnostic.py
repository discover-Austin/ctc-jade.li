"""
Diagnostic codes and OBD-II API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.db.base import get_db
from app.models.diagnostic import DiagnosticCode, OBD2PID, LiveDataRange
from app.schemas.diagnostic import (
    DTCResponse,
    DTCSearchRequest,
    OBD2PIDResponse,
    LiveDataRangeResponse
)

router = APIRouter()


@router.get("/dtc/{vehicle_id}/{code}", response_model=DTCResponse)
async def get_diagnostic_code(
    vehicle_id: UUID,
    code: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve detailed information about a specific DTC code.

    - **vehicle_id**: UUID of the vehicle
    - **code**: DTC code (e.g., P0300, B1234, C0035, U0100)

    Returns comprehensive diagnostic information including:
    - Code description and symptoms
    - Possible causes
    - Step-by-step diagnostic procedures
    - Component test specifications
    - Related repair procedures
    - Commonly replaced parts
    - TSB references
    - Freeze frame data parameters
    - Drive cycle requirements
    """
    code = code.upper()

    dtc = db.query(DiagnosticCode).filter(
        DiagnosticCode.vehicle_id == vehicle_id,
        DiagnosticCode.code == code
    ).first()

    if not dtc:
        raise HTTPException(
            status_code=404,
            detail=f"DTC code {code} not found for this vehicle"
        )

    return dtc


@router.get("/dtc/search/{vehicle_id}", response_model=List[DTCResponse])
async def search_diagnostic_codes(
    vehicle_id: UUID,
    code: Optional[str] = Query(None, description="DTC code or partial match"),
    system: Optional[str] = Query(None, description="System (Engine, Transmission, etc.)"),
    severity: Optional[str] = Query(None, description="Severity level"),
    emission_related: Optional[bool] = Query(None, description="Filter emission-related codes"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Search diagnostic trouble codes with filters.

    Optional filters:
    - **code**: Full or partial DTC code (e.g., "P03" matches P0300, P0301, etc.)
    - **system**: Filter by system
    - **severity**: Filter by severity (Critical, Important, Minor)
    - **emission_related**: Filter emission-related codes only
    - **limit**: Maximum results
    - **offset**: Pagination offset
    """
    query = db.query(DiagnosticCode).filter(DiagnosticCode.vehicle_id == vehicle_id)

    if code:
        query = query.filter(DiagnosticCode.code.ilike(f"%{code.upper()}%"))

    if system:
        query = query.filter(DiagnosticCode.system.ilike(f"%{system}%"))

    if severity:
        query = query.filter(DiagnosticCode.severity == severity)

    if emission_related is not None:
        query = query.filter(DiagnosticCode.emission_related == emission_related)

    dtc_codes = query.offset(offset).limit(limit).all()

    return dtc_codes


@router.get("/dtc/types")
async def get_dtc_types():
    """
    Get information about DTC code types.

    Returns:
    - P codes: Powertrain (engine, transmission)
    - B codes: Body (airbags, climate control, etc.)
    - C codes: Chassis (ABS, suspension, steering)
    - U codes: Network/Communication (CAN bus, modules)
    """
    return {
        "types": [
            {
                "code": "P",
                "name": "Powertrain",
                "description": "Engine, transmission, and emissions-related codes",
                "examples": ["P0300 - Random/Multiple Cylinder Misfire", "P0420 - Catalyst System Efficiency"]
            },
            {
                "code": "B",
                "name": "Body",
                "description": "Body systems including airbags, climate control, and accessories",
                "examples": ["B0001 - Driver Airbag Circuit", "B1318 - Battery Voltage Low"]
            },
            {
                "code": "C",
                "name": "Chassis",
                "description": "ABS, suspension, steering, and chassis systems",
                "examples": ["C0035 - Left Front Wheel Speed Sensor", "C1234 - ABS Pump Motor"]
            },
            {
                "code": "U",
                "name": "Network/Communication",
                "description": "Communication between vehicle modules",
                "examples": ["U0100 - Lost Communication with ECM", "U0155 - Lost Communication with IPC"]
            }
        ]
    }


@router.get("/obd2/pids/{vehicle_id}", response_model=List[OBD2PIDResponse])
async def get_obd2_pids(
    vehicle_id: UUID,
    service_mode: Optional[str] = Query(None, description="OBD-II service mode (01, 02, etc.)"),
    supported_only: bool = Query(True, description="Show only supported PIDs"),
    db: Session = Depends(get_db)
):
    """
    Get supported OBD-II PIDs (Parameter IDs) for a vehicle.

    Optional filters:
    - **service_mode**: Filter by OBD-II service mode (01, 02, 03, etc.)
    - **supported_only**: Show only PIDs supported by this vehicle

    Returns PID information including:
    - PID code and description
    - Service mode
    - Data bytes and scaling formula
    - Units and value ranges
    - Update rate
    """
    query = db.query(OBD2PID).filter(OBD2PID.vehicle_id == vehicle_id)

    if service_mode:
        query = query.filter(OBD2PID.service_mode == service_mode)

    if supported_only:
        query = query.filter(OBD2PID.supported == True)

    pids = query.all()

    return pids


@router.get("/obd2/modes")
async def get_obd2_modes():
    """
    Get information about OBD-II service modes.

    Returns descriptions of all standard OBD-II modes:
    - Mode 01: Current data
    - Mode 02: Freeze frame data
    - Mode 03: Stored DTCs
    - Mode 04: Clear DTCs
    - Mode 05: O2 sensor monitoring
    - Mode 06: On-board monitoring test results
    - Mode 07: Pending DTCs
    - Mode 08: Control of on-board systems
    - Mode 09: Vehicle information
    """
    return {
        "modes": [
            {"mode": "01", "name": "Current Data", "description": "Request current powertrain diagnostic data"},
            {"mode": "02", "name": "Freeze Frame Data", "description": "Request powertrain freeze frame data"},
            {"mode": "03", "name": "Stored DTCs", "description": "Request emission-related DTCs"},
            {"mode": "04", "name": "Clear DTCs", "description": "Clear/reset DTCs and stored values"},
            {"mode": "05", "name": "O2 Sensor Monitoring", "description": "Request oxygen sensor monitoring test results"},
            {"mode": "06", "name": "Test Results", "description": "Request on-board monitoring test results"},
            {"mode": "07", "name": "Pending DTCs", "description": "Request pending DTCs"},
            {"mode": "08", "name": "Control Systems", "description": "Request control of on-board systems"},
            {"mode": "09", "name": "Vehicle Information", "description": "Request vehicle information (VIN, calibration IDs)"},
            {"mode": "0A", "name": "Permanent DTCs", "description": "Request permanent DTCs"}
        ]
    }


@router.get("/live-data/{vehicle_id}", response_model=List[LiveDataRangeResponse])
async def get_live_data_ranges(
    vehicle_id: UUID,
    parameter: Optional[str] = Query(None, description="Filter by parameter name"),
    condition: Optional[str] = Query(None, description="Filter by condition (Idle, Cruise, WOT)"),
    db: Session = Depends(get_db)
):
    """
    Get typical live data ranges for diagnostic parameters.

    Optional filters:
    - **parameter**: Filter by parameter name (e.g., "RPM", "MAF", "O2 Sensor")
    - **condition**: Filter by engine condition (Idle, Cruise, WOT, etc.)

    Returns typical ranges for diagnostic parameters including:
    - Parameter name and PID
    - Operating condition
    - Typical value
    - Normal min/max range
    - Units
    """
    query = db.query(LiveDataRange).filter(LiveDataRange.vehicle_id == vehicle_id)

    if parameter:
        query = query.filter(LiveDataRange.parameter_name.ilike(f"%{parameter}%"))

    if condition:
        query = query.filter(LiveDataRange.condition.ilike(f"%{condition}%"))

    ranges = query.all()

    return ranges


@router.get("/conditions")
async def get_diagnostic_conditions():
    """
    Get list of standard diagnostic conditions for live data.

    Returns:
    - Operating conditions used for diagnostic parameters
    - Typical RPM ranges for each condition
    """
    return {
        "conditions": [
            {"name": "Idle", "description": "Engine at idle speed", "typical_rpm": "600-900"},
            {"name": "Cruise", "description": "Steady highway speed", "typical_rpm": "2000-2500"},
            {"name": "WOT", "description": "Wide Open Throttle / Full acceleration", "typical_rpm": "5000-7000"},
            {"name": "Decel", "description": "Deceleration / Overrun", "typical_rpm": "Variable"},
            {"name": "Cold Start", "description": "Engine cold start condition", "typical_rpm": "800-1500"},
            {"name": "Hot Idle", "description": "Engine at operating temperature, idle", "typical_rpm": "600-800"}
        ]
    }
