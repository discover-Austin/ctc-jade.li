"""
Repair procedures, torque specifications, and maintenance schedules.
"""
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, ForeignKey, Text, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class RepairProcedure(Base):
    """Service procedures master table."""

    __tablename__ = "repair_procedures"

    procedure_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False, index=True)
    system_category = Column(String(100), index=True, comment="Engine, Transmission, Brakes, etc.")
    subsystem = Column(String(100))
    procedure_name = Column(String(255), nullable=False, index=True)
    difficulty_level = Column(String(20), comment="Beginner, Intermediate, Advanced, Professional")
    estimated_time_hours = Column(DECIMAL(3, 1))
    labor_time_oem_hours = Column(DECIMAL(3, 1), comment="OEM flat rate time")
    special_tools_required = Column(JSONB, comment="Array of tool descriptions")
    safety_precautions = Column(Text)
    prerequisites = Column(Text, comment="Other procedures that must be done first")
    procedure_steps = Column(JSONB, comment="Detailed step-by-step instructions")
    torque_specifications = Column(JSONB, comment="All fasteners with values")
    clearance_specifications = Column(JSONB)
    wear_limits = Column(JSONB)
    parts_required = Column(JSONB, comment="Parts list with OEM numbers")
    consumables_required = Column(JSONB, comment="Fluids, gaskets, sealants")
    wiring_diagrams = Column(JSONB, comment="References to diagram IDs")
    photos = Column(JSONB, comment="Array of image URLs")
    videos = Column(JSONB, comment="Array of video URLs")
    technical_notes = Column(Text)
    common_mistakes = Column(Text)
    tips_and_tricks = Column(Text)
    related_dtc_codes = Column(JSONB, comment="Related diagnostic codes")
    tsb_references = Column(JSONB, comment="Technical service bulletin references")
    revision_number = Column(Integer, default=1)
    revision_date = Column(Date)
    verified_by = Column(String(255))
    source = Column(String(255), comment="OEM, Aftermarket, Community")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    vehicle = relationship("Vehicle", back_populates="repair_procedures")

    def __repr__(self):
        return f"<RepairProcedure {self.procedure_name}>"


class TorqueSpec(Base):
    """Torque specifications comprehensive table."""

    __tablename__ = "torque_specs"

    torque_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False, index=True)
    component_name = Column(String(255), nullable=False, index=True)
    fastener_description = Column(String(255))
    torque_lb_ft = Column(Integer)
    torque_nm = Column(Integer)
    torque_sequence = Column(String(20), comment="Sequential, Cross-pattern, etc.")
    sequence_diagram_url = Column(Text)
    additional_procedures = Column(Text, comment="Angle torque, stretch bolts, etc.")
    thread_locker_required = Column(Boolean)
    thread_locker_type = Column(String(100))
    lubrication_required = Column(Boolean)
    lubrication_type = Column(String(100))
    reusability = Column(String(50), comment="Reusable, Replace, Inspect")
    system_category = Column(String(100), index=True)
    notes = Column(Text)

    # Relationship
    vehicle = relationship("Vehicle")

    def __repr__(self):
        return f"<TorqueSpec {self.component_name}: {self.torque_lb_ft} lb-ft>"


class MaintenanceSchedule(Base):
    """Maintenance schedules table."""

    __tablename__ = "maintenance_schedules"

    schedule_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False, index=True)
    service_item = Column(String(255), nullable=False)
    interval_miles = Column(Integer, index=True)
    interval_months = Column(Integer)
    interval_type = Column(String(50), comment="Normal, Severe")
    description = Column(Text)
    procedure_reference = Column(UUID(as_uuid=True), ForeignKey("repair_procedures.procedure_id"))
    parts_required = Column(JSONB)
    fluids_required = Column(JSONB)
    estimated_cost_range = Column(String(50))
    priority = Column(String(20), comment="Critical, Important, Recommended")
    inspection_points = Column(Text)
    notes = Column(Text)

    # Relationship
    vehicle = relationship("Vehicle")
    repair_procedure = relationship("RepairProcedure")

    def __repr__(self):
        return f"<MaintenanceSchedule {self.service_item} at {self.interval_miles} miles>"
