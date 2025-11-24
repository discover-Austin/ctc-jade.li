"""
Electrical system and wiring diagram models.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class ElectricalSystem(Base):
    """Electrical system specifications table."""

    __tablename__ = "electrical_systems"

    electrical_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False)
    battery_voltage = Column(Integer)
    battery_cca = Column(Integer, comment="Cold cranking amps")
    battery_group_size = Column(String(20))
    battery_type = Column(String(50), comment="Lead-acid, AGM, Lithium")
    alternator_amperage = Column(Integer)
    starter_type = Column(String(100))
    ignition_system = Column(String(100), comment="Coil-on-plug, distributor, etc.")
    spark_plug_type = Column(String(100))
    spark_plug_gap_mm = Column(String(10))
    spark_plug_torque_lb_ft = Column(Integer)
    fuse_box_locations = Column(JSONB, comment="Array of locations with diagrams")
    relay_locations = Column(JSONB)
    ground_points = Column(JSONB)
    can_bus_protocol = Column(String(50), comment="CAN-HS, CAN-LS, LIN, etc.")
    obd2_location = Column(String(200))
    communication_protocols = Column(JSONB, comment="Various network protocols")

    # Relationship
    vehicle = relationship("Vehicle", back_populates="electrical_systems")

    def __repr__(self):
        return f"<ElectricalSystem {self.battery_voltage}V for vehicle {self.vehicle_id}>"


class WiringDiagram(Base):
    """Wiring diagrams and electrical schematics table."""

    __tablename__ = "wiring_diagrams"

    diagram_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False)
    system_name = Column(String(255), nullable=False, index=True)
    subsystem = Column(String(255))
    diagram_type = Column(String(50), comment="Schematic, Location, Connector")
    year_applicable_start = Column(Integer)
    year_applicable_end = Column(Integer)
    diagram_file_url = Column(Text, nullable=False, comment="High-res image or PDF")
    diagram_format = Column(String(20), comment="SVG, PDF, PNG")
    connector_locations = Column(JSONB)
    wire_colors = Column(JSONB, comment="Color codes and gauges")
    component_locations = Column(JSONB)
    ground_locations = Column(JSONB)
    splice_locations = Column(JSONB)
    fuse_references = Column(JSONB)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    vehicle = relationship("Vehicle")

    def __repr__(self):
        return f"<WiringDiagram {self.system_name} for vehicle {self.vehicle_id}>"


class SensorSpecification(Base):
    """Sensor specifications and test procedures table."""

    __tablename__ = "sensor_specifications"

    sensor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False)
    sensor_name = Column(String(255), nullable=False)
    sensor_type = Column(String(100), comment="MAF, O2, TPS, etc.")
    location = Column(String(255))
    part_number = Column(String(100))
    resistance_spec = Column(JSONB, comment="Resistance at various temps")
    voltage_spec = Column(JSONB, comment="Voltage ranges")
    frequency_spec = Column(JSONB, comment="For some sensors")
    test_procedure = Column(Text)
    common_failure_modes = Column(Text)
    replacement_interval_miles = Column(Integer)
    diagnostic_procedure = Column(Text)
    wiring_diagram_reference = Column(UUID(as_uuid=True))

    # Relationship
    vehicle = relationship("Vehicle")

    def __repr__(self):
        return f"<SensorSpecification {self.sensor_name}>"
