"""
Fluid, HVAC, and fuel system models.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class FluidSpecification(Base):
    """Fluid specifications table."""

    __tablename__ = "fluid_specifications"

    fluid_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False)
    fluid_type = Column(String(100), nullable=False, comment="Engine oil, Coolant, etc.")
    oem_specification = Column(String(255), comment="API SN, ACEA C3, etc.")
    viscosity = Column(String(50), comment="5W-30, 0W-20, etc.")
    capacity_quarts = Column(DECIMAL(4, 2))
    capacity_liters = Column(DECIMAL(4, 2))
    drain_fill_capacity_quarts = Column(DECIMAL(4, 2))
    service_interval_miles = Column(Integer)
    service_interval_months = Column(Integer)
    replacement_procedure = Column(Text)
    compatible_brands = Column(JSONB, comment="Array of approved brands")
    oem_part_numbers = Column(JSONB)
    color = Column(String(50))
    special_requirements = Column(Text)
    notes = Column(Text)

    # Relationship
    vehicle = relationship("Vehicle")

    def __repr__(self):
        return f"<FluidSpecification {self.fluid_type} for vehicle {self.vehicle_id}>"


class HVACSystem(Base):
    """HVAC system specifications table."""

    __tablename__ = "hvac_systems"

    hvac_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False)
    refrigerant_type = Column(String(20), comment="R-134a, R-1234yf")
    refrigerant_capacity_oz = Column(DECIMAL(5, 2))
    compressor_oil_type = Column(String(100))
    compressor_oil_capacity_oz = Column(DECIMAL(4, 2))
    compressor_clutch_gap_mm = Column(DECIMAL(3, 2))
    condenser_type = Column(String(50))
    evaporator_type = Column(String(50))
    expansion_valve_type = Column(String(50), comment="Orifice tube, TXV")
    cabin_filter_location = Column(String(200))
    cabin_filter_part_number = Column(String(100))
    blower_motor_location = Column(String(200))
    climate_control_type = Column(String(50), comment="Manual, Automatic, Dual-zone, etc.")

    # Relationship
    vehicle = relationship("Vehicle", back_populates="hvac_systems")

    def __repr__(self):
        return f"<HVACSystem {self.refrigerant_type} for vehicle {self.vehicle_id}>"


class FuelSystem(Base):
    """Fuel system specifications table."""

    __tablename__ = "fuel_systems"

    fuel_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False)
    fuel_type = Column(String(50), comment="Regular, Premium, Diesel, E85, etc.")
    fuel_octane_rating = Column(Integer)
    tank_capacity_gallons = Column(DECIMAL(4, 2))
    fuel_pump_type = Column(String(100))
    fuel_pump_pressure_psi = Column(Integer)
    fuel_filter_location = Column(String(200))
    fuel_filter_change_interval = Column(Integer)
    injector_type = Column(String(100))
    injector_ohms = Column(DECIMAL(4, 2))
    fuel_rail_pressure_psi = Column(Integer)
    evaporative_system = Column(String(100))
    purge_valve_location = Column(String(200))

    # Relationship
    vehicle = relationship("Vehicle", back_populates="fuel_systems")

    def __repr__(self):
        return f"<FuelSystem {self.fuel_type} for vehicle {self.vehicle_id}>"
