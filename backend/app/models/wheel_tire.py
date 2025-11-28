"""
Wheel and tire specifications model.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class WheelTireSpec(Base):
    """Wheel and tire specifications table."""

    __tablename__ = "wheel_tire_specs"

    spec_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False)
    wheel_diameter_inches = Column(Integer)
    wheel_width_inches = Column(DECIMAL(4, 1))
    bolt_pattern = Column(String(20), comment="5x114.3, 6x139.7, etc.")
    center_bore_mm = Column(DECIMAL(5, 2), comment="Hub bore diameter")
    hub_bore_mm = Column(DECIMAL(5, 2))  # Alias for center_bore_mm
    wheel_offset_mm = Column(Integer)
    offset_mm = Column(Integer)  # Alias for wheel_offset_mm
    tire_size_front = Column(String(50), comment="235/45R18, etc.")
    tire_size_rear = Column(String(50))
    tire_pressure_front_psi = Column(Integer)
    tire_pressure_rear_psi = Column(Integer)
    tpms_type = Column(String(50), comment="Direct, Indirect")
    tpms_frequency_mhz = Column(DECIMAL(6, 3))
    lug_nut_torque_lb_ft = Column(Integer)
    wheel_material = Column(String(50), comment="Alloy, Steel, Aluminum Alloy")
    spare_tire_type = Column(String(50))

    # Relationship
    vehicle = relationship("Vehicle", back_populates="wheel_tire_specs")

    def __repr__(self):
        return f"<WheelTireSpec {self.tire_size_front} for vehicle {self.vehicle_id}>"
