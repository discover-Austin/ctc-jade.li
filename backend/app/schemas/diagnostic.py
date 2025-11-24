"""
Pydantic schemas for diagnostic codes and OBD-II data.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID


class DTCResponse(BaseModel):
    """Schema for DTC (Diagnostic Trouble Code) response."""

    dtc_id: UUID
    vehicle_id: UUID
    code: str
    code_type: Optional[str] = None
    system: Optional[str] = None
    description: str
    symptoms: Optional[str] = None
    possible_causes: List[str] = []
    diagnostic_steps: List[Dict[str, Any]] = []
    component_tests: List[Dict[str, Any]] = []
    repair_procedures: List[UUID] = []
    parts_commonly_replaced: List[Dict[str, Any]] = []
    tsb_references: List[str] = []
    freeze_frame_data: Optional[Dict[str, Any]] = None
    monitor_readiness: Optional[str] = None
    obd2_test_mode: Optional[str] = None
    severity: Optional[str] = None
    emission_related: Optional[bool] = None
    drive_cycle_requirements: Optional[str] = None
    clear_code_procedure: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class DTCSearchRequest(BaseModel):
    """Schema for DTC search request."""

    code: Optional[str] = None
    system: Optional[str] = None
    severity: Optional[str] = None
    emission_related: Optional[bool] = None


class OBD2PIDResponse(BaseModel):
    """Schema for OBD-II PID response."""

    pid_id: UUID
    vehicle_id: UUID
    pid_code: str
    service_mode: Optional[str] = None
    description: Optional[str] = None
    data_bytes: Optional[int] = None
    scaling_formula: Optional[str] = None
    units: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    supported: bool = True
    update_rate_hz: Optional[float] = None

    class Config:
        from_attributes = True


class LiveDataRangeResponse(BaseModel):
    """Schema for live data range response."""

    range_id: UUID
    vehicle_id: UUID
    parameter_name: str
    parameter_pid: Optional[str] = None
    condition: Optional[str] = None
    typical_value: Optional[float] = None
    normal_range_min: Optional[float] = None
    normal_range_max: Optional[float] = None
    units: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
