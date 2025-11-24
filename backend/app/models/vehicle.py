"""
Vehicle-related database models including engines, transmissions, suspension, and brakes.
"""
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, ForeignKey, DECIMAL, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class Vehicle(Base):
    """Primary vehicle registry table."""

    __tablename__ = "vehicles"

    vehicle_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vin_pattern = Column(String(17), index=True, comment="VIN decoding patterns")
    year = Column(Integer, nullable=False, index=True, comment="Model year")
    make = Column(String(100), nullable=False, index=True)
    model = Column(String(100), nullable=False, index=True)
    trim = Column(String(100))
    body_style = Column(String(50), comment="Sedan, SUV, Truck, Coupe, etc.")
    drive_type = Column(String(20), comment="FWD, RWD, AWD, 4WD")
    transmission_type = Column(String(50))
    engine_config = Column(String(50), comment="Engine code/designation")
    production_start = Column(Date)
    production_end = Column(Date)
    market_region = Column(String(50), comment="US, Europe, Asia, etc.")
    platform_code = Column(String(50), comment="Manufacturer platform designation")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    data_verified = Column(Boolean, default=False)
    verification_source = Column(String(255))

    # Relationships
    engines = relationship("Engine", back_populates="vehicle", cascade="all, delete-orphan")
    transmissions = relationship("Transmission", back_populates="vehicle", cascade="all, delete-orphan")
    suspension_systems = relationship("SuspensionSystem", back_populates="vehicle", cascade="all, delete-orphan")
    brake_systems = relationship("BrakeSystem", back_populates="vehicle", cascade="all, delete-orphan")
    wheel_tire_specs = relationship("WheelTireSpec", back_populates="vehicle", cascade="all, delete-orphan")
    electrical_systems = relationship("ElectricalSystem", back_populates="vehicle", cascade="all, delete-orphan")
    hvac_systems = relationship("HVACSystem", back_populates="vehicle", cascade="all, delete-orphan")
    fuel_systems = relationship("FuelSystem", back_populates="vehicle", cascade="all, delete-orphan")
    repair_procedures = relationship("RepairProcedure", back_populates="vehicle", cascade="all, delete-orphan")
    diagnostic_codes = relationship("DiagnosticCode", back_populates="vehicle", cascade="all, delete-orphan")
    technical_bulletins = relationship("TechnicalBulletin", back_populates="vehicle", cascade="all, delete-orphan")
    recalls = relationship("Recall", back_populates="vehicle", cascade="all, delete-orphan")
    common_problems = relationship("CommonProblem", back_populates="vehicle", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Vehicle {self.year} {self.make} {self.model}>"


class Engine(Base):
    """Engine specifications table."""

    __tablename__ = "engines"

    engine_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False)
    engine_code = Column(String(50), nullable=False, comment="Manufacturer designation")
    displacement_liters = Column(DECIMAL(3, 1))
    displacement_cc = Column(Integer)
    cylinders = Column(Integer)
    configuration = Column(String(50), comment="Inline-4, V6, V8, Boxer, etc.")
    aspiration = Column(String(50), comment="Naturally Aspirated, Turbo, Supercharged")
    fuel_system = Column(String(100), comment="Direct injection, port injection, etc.")
    horsepower = Column(Integer)
    horsepower_rpm = Column(Integer)
    torque_lb_ft = Column(Integer)
    torque_rpm = Column(Integer)
    compression_ratio = Column(DECIMAL(4, 2))
    bore_mm = Column(DECIMAL(5, 2))
    stroke_mm = Column(DECIMAL(5, 2))
    firing_order = Column(String(20))
    valve_train = Column(String(100), comment="DOHC, SOHC, VVT systems")
    camshaft_specs = Column(JSONB, comment="Timing, lift, duration")
    emissions_standard = Column(String(50), comment="EPA Tier 3, Euro 6, etc.")
    hybrid_system = Column(Boolean, default=False)
    hybrid_type = Column(String(50), comment="Parallel, Series, Plug-in")
    battery_kwh = Column(DECIMAL(5, 2), comment="For EVs/PHEVs")
    electric_motor_hp = Column(Integer)
    electric_range_miles = Column(Integer)

    # Relationship
    vehicle = relationship("Vehicle", back_populates="engines")

    def __repr__(self):
        return f"<Engine {self.engine_code} - {self.displacement_liters}L>"


class Transmission(Base):
    """Transmission specifications table."""

    __tablename__ = "transmissions"

    transmission_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False)
    transmission_code = Column(String(50))
    type = Column(String(50), comment="Manual, Automatic, CVT, DCT")
    speeds = Column(Integer)
    final_drive_ratio = Column(DECIMAL(4, 3))
    gear_ratios = Column(JSONB, comment="Array of gear ratios")
    torque_converter_specs = Column(JSONB)
    transfer_case_ratios = Column(JSONB, comment="For 4WD/AWD")
    fluid_type = Column(String(100))
    fluid_capacity_quarts = Column(DECIMAL(4, 2))
    service_interval_miles = Column(Integer)
    manufacturer = Column(String(100))

    # Relationship
    vehicle = relationship("Vehicle", back_populates="transmissions")

    def __repr__(self):
        return f"<Transmission {self.transmission_code} - {self.speeds}-speed {self.type}>"


class SuspensionSystem(Base):
    """Suspension and chassis specifications table."""

    __tablename__ = "suspension_systems"

    suspension_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False)
    front_suspension = Column(String(200))
    rear_suspension = Column(String(200))
    front_spring_type = Column(String(50))
    rear_spring_type = Column(String(50))
    shock_absorber_type = Column(String(100))
    stabilizer_bar_diameter_mm = Column(DECIMAL(4, 1))
    steering_type = Column(String(100), comment="Rack and pinion, recirculating ball")
    steering_ratio = Column(DECIMAL(4, 2))
    turning_radius_ft = Column(DECIMAL(4, 1))
    ride_height_mm = Column(Integer)
    ground_clearance_mm = Column(Integer)
    track_width_front_mm = Column(Integer)
    track_width_rear_mm = Column(Integer)
    wheelbase_mm = Column(Integer)
    adaptive_suspension = Column(Boolean, default=False)
    adjustable_damping = Column(Boolean, default=False)

    # Relationship
    vehicle = relationship("Vehicle", back_populates="suspension_systems")

    def __repr__(self):
        return f"<SuspensionSystem for vehicle {self.vehicle_id}>"


class BrakeSystem(Base):
    """Brake system specifications table."""

    __tablename__ = "brake_systems"

    brake_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False)
    front_brake_type = Column(String(50), comment="Disc, Drum")
    rear_brake_type = Column(String(50))
    front_rotor_diameter_mm = Column(DECIMAL(5, 2))
    front_rotor_thickness_mm = Column(DECIMAL(4, 2))
    rear_rotor_diameter_mm = Column(DECIMAL(5, 2))
    rear_rotor_thickness_mm = Column(DECIMAL(4, 2))
    caliper_type = Column(String(50), comment="Floating, Fixed")
    piston_count_front = Column(Integer)
    piston_count_rear = Column(Integer)
    parking_brake_type = Column(String(50), comment="Mechanical, Electronic")
    abs_system = Column(String(100))
    traction_control = Column(Boolean, default=True)
    stability_control = Column(Boolean, default=True)
    brake_fluid_type = Column(String(50), comment="DOT 3, DOT 4, DOT 5.1")
    fluid_capacity_oz = Column(DECIMAL(4, 2))

    # Relationship
    vehicle = relationship("Vehicle", back_populates="brake_systems")

    def __repr__(self):
        return f"<BrakeSystem for vehicle {self.vehicle_id}>"
