"""
Diagnostic trouble codes (DTC), OBD-II PIDs, and live data ranges.
"""
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class DiagnosticCode(Base):
    """Diagnostic Trouble Codes (DTC) table."""

    __tablename__ = "diagnostic_codes"

    dtc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False, index=True)
    code = Column(String(10), nullable=False, index=True, comment="P0301, B1234, etc.")
    code_type = Column(String(10), comment="P, B, C, U (Powertrain, Body, Chassis, Network)")
    system = Column(String(100))
    description = Column(Text, nullable=False)
    symptoms = Column(Text)
    possible_causes = Column(JSONB, comment="Array of causes")
    diagnostic_steps = Column(JSONB, comment="Step-by-step diagnosis")
    component_tests = Column(JSONB, comment="Electrical tests, resistance values")
    repair_procedures = Column(JSONB, comment="References to repair_procedures")
    parts_commonly_replaced = Column(JSONB)
    tsb_references = Column(JSONB)
    freeze_frame_data = Column(JSONB, comment="Important parameters to check")
    monitor_readiness = Column(Text)
    obd2_test_mode = Column(String(50), comment="Mode 01, 02, etc.")
    severity = Column(String(20), comment="Critical, Important, Minor")
    emission_related = Column(Boolean)
    drive_cycle_requirements = Column(Text)
    clear_code_procedure = Column(Text)
    notes = Column(Text)

    # Relationship
    vehicle = relationship("Vehicle", back_populates="diagnostic_codes")

    def __repr__(self):
        return f"<DiagnosticCode {self.code}: {self.description[:50]}>"


class OBD2PID(Base):
    """OBD-II PID (Parameter ID) support table."""

    __tablename__ = "obd2_pids"

    pid_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False, index=True)
    pid_code = Column(String(10), nullable=False, comment="0100, 010C, etc.")
    service_mode = Column(String(10), comment="01, 02, 03, etc.")
    description = Column(String(255))
    data_bytes = Column(Integer)
    scaling_formula = Column(Text)
    units = Column(String(50))
    min_value = Column(DECIMAL(10, 3))
    max_value = Column(DECIMAL(10, 3))
    supported = Column(Boolean, default=True)
    update_rate_hz = Column(DECIMAL(4, 1))

    # Relationship
    vehicle = relationship("Vehicle")

    def __repr__(self):
        return f"<OBD2PID {self.pid_code}: {self.description}>"


class LiveDataRange(Base):
    """Live data typical ranges table."""

    __tablename__ = "live_data_ranges"

    range_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False, index=True)
    parameter_name = Column(String(255), nullable=False)
    parameter_pid = Column(String(10))
    condition = Column(String(100), comment="Idle, Cruise, WOT, etc.")
    typical_value = Column(DECIMAL(10, 3))
    normal_range_min = Column(DECIMAL(10, 3))
    normal_range_max = Column(DECIMAL(10, 3))
    units = Column(String(50))
    notes = Column(Text)

    # Relationship
    vehicle = relationship("Vehicle")

    def __repr__(self):
        return f"<LiveDataRange {self.parameter_name} at {self.condition}>"
