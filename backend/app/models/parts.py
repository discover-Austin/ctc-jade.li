"""
Parts catalog and cross-reference model.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Text, DECIMAL
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base


class PartsCatalog(Base):
    """Parts cross-reference table."""

    __tablename__ = "parts_catalog"

    part_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False, index=True)
    oem_part_number = Column(String(100), nullable=False, index=True)
    part_name = Column(String(255), nullable=False, index=True)
    part_category = Column(String(100), index=True)
    description = Column(Text)
    superseded_by = Column(String(100), comment="Newer part number")
    supersedes = Column(String(100), comment="Older part number")
    interchange_numbers = Column(JSONB, comment="Aftermarket equivalents")
    compatible_brands = Column(JSONB)
    average_price_usd = Column(DECIMAL(8, 2))
    typical_lifespan_miles = Column(Integer)
    weight_lbs = Column(DECIMAL(6, 2))
    dimensions = Column(JSONB)
    notes = Column(Text)
    image_urls = Column(JSONB)

    # Relationship
    vehicle = relationship("Vehicle")

    def __repr__(self):
        return f"<PartsCatalog {self.oem_part_number}: {self.part_name}>"
