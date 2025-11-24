"""
Pydantic schemas for repair procedures and maintenance.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal


class RepairProcedureBase(BaseModel):
    """Base repair procedure schema."""

    system_category: str = Field(..., max_length=100)
    subsystem: Optional[str] = Field(None, max_length=100)
    procedure_name: str = Field(..., max_length=255)
    difficulty_level: str = Field(..., max_length=20)
    estimated_time_hours: Optional[Decimal] = None
    labor_time_oem_hours: Optional[Decimal] = None


class RepairProcedureCreate(RepairProcedureBase):
    """Schema for creating a repair procedure."""

    vehicle_id: UUID
    special_tools_required: Optional[List[str]] = []
    safety_precautions: Optional[str] = None
    prerequisites: Optional[str] = None
    procedure_steps: Optional[List[Dict[str, Any]]] = []
    torque_specifications: Optional[List[Dict[str, Any]]] = []
    clearance_specifications: Optional[Dict[str, Any]] = None
    wear_limits: Optional[Dict[str, Any]] = None
    parts_required: Optional[List[Dict[str, Any]]] = []
    consumables_required: Optional[List[Dict[str, Any]]] = []
    wiring_diagrams: Optional[List[UUID]] = []
    photos: Optional[List[str]] = []
    videos: Optional[List[str]] = []
    technical_notes: Optional[str] = None
    common_mistakes: Optional[str] = None
    tips_and_tricks: Optional[str] = None
    related_dtc_codes: Optional[List[str]] = []
    tsb_references: Optional[List[str]] = []
    verified_by: Optional[str] = None
    source: Optional[str] = None


class RepairProcedureResponse(RepairProcedureBase):
    """Schema for repair procedure response."""

    procedure_id: UUID
    vehicle_id: UUID
    special_tools_required: List[str] = []
    safety_precautions: Optional[str] = None
    prerequisites: Optional[str] = None
    procedure_steps: List[Dict[str, Any]] = []
    torque_specifications: List[Dict[str, Any]] = []
    clearance_specifications: Optional[Dict[str, Any]] = None
    wear_limits: Optional[Dict[str, Any]] = None
    parts_required: List[Dict[str, Any]] = []
    consumables_required: List[Dict[str, Any]] = []
    wiring_diagrams: List[UUID] = []
    photos: List[str] = []
    videos: List[str] = []
    technical_notes: Optional[str] = None
    common_mistakes: Optional[str] = None
    tips_and_tricks: Optional[str] = None
    related_dtc_codes: List[str] = []
    tsb_references: List[str] = []
    revision_number: int
    revision_date: Optional[date] = None
    verified_by: Optional[str] = None
    source: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TorqueSpecResponse(BaseModel):
    """Schema for torque specification response."""

    torque_id: UUID
    vehicle_id: UUID
    component_name: str
    fastener_description: Optional[str] = None
    torque_lb_ft: Optional[int] = None
    torque_nm: Optional[int] = None
    torque_sequence: Optional[str] = None
    sequence_diagram_url: Optional[str] = None
    additional_procedures: Optional[str] = None
    thread_locker_required: Optional[bool] = None
    thread_locker_type: Optional[str] = None
    lubrication_required: Optional[bool] = None
    lubrication_type: Optional[str] = None
    reusability: Optional[str] = None
    system_category: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class MaintenanceScheduleResponse(BaseModel):
    """Schema for maintenance schedule response."""

    schedule_id: UUID
    vehicle_id: UUID
    service_item: str
    interval_miles: Optional[int] = None
    interval_months: Optional[int] = None
    interval_type: Optional[str] = None
    description: Optional[str] = None
    procedure_reference: Optional[UUID] = None
    parts_required: Optional[List[Dict[str, Any]]] = []
    fluids_required: Optional[List[Dict[str, Any]]] = []
    estimated_cost_range: Optional[str] = None
    priority: Optional[str] = None
    inspection_points: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
