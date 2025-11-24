"""
Technical service bulletins, recalls, and common problems.
"""
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class TechnicalBulletin(Base):
    """Technical Service Bulletins table."""

    __tablename__ = "technical_bulletins"

    tsb_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False, index=True)
    bulletin_number = Column(String(50), nullable=False, index=True)
    issue_date = Column(Date)
    title = Column(String(500), nullable=False)
    category = Column(String(100), index=True)
    affected_components = Column(JSONB)
    symptom_description = Column(Text)
    condition_description = Column(Text)
    root_cause = Column(Text)
    correction_procedure = Column(Text)
    parts_required = Column(JSONB)
    special_tools_required = Column(JSONB)
    warranty_information = Column(Text)
    related_dtc_codes = Column(JSONB)
    supersedes_bulletins = Column(JSONB, comment="Previous bulletin numbers")
    bulletin_pdf_url = Column(Text)
    manufacturer_official = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship
    vehicle = relationship("Vehicle", back_populates="technical_bulletins")

    def __repr__(self):
        return f"<TechnicalBulletin {self.bulletin_number}: {self.title[:50]}>"


class Recall(Base):
    """Recalls and safety campaigns table."""

    __tablename__ = "recalls"

    recall_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False, index=True)
    nhtsa_campaign_number = Column(String(50), index=True)
    manufacturer_recall_number = Column(String(50))
    recall_date = Column(Date)
    recall_type = Column(String(50), comment="Safety, Compliance, Emissions")
    component = Column(String(255))
    summary = Column(Text)
    consequence = Column(Text)
    remedy = Column(Text)
    affected_vin_ranges = Column(JSONB)
    affected_quantity = Column(Integer)
    recall_status = Column(String(50), comment="Active, Completed, Pending")
    remedy_available_date = Column(Date)
    bulletin_pdf_url = Column(Text)
    notes = Column(Text)

    # Relationship
    vehicle = relationship("Vehicle", back_populates="recalls")

    def __repr__(self):
        return f"<Recall {self.nhtsa_campaign_number}: {self.component}>"


class CommonProblem(Base):
    """Common problems and solutions table."""

    __tablename__ = "common_problems"

    problem_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.vehicle_id"), nullable=False, index=True)
    problem_title = Column(String(255), nullable=False)
    problem_category = Column(String(100), index=True)
    symptoms = Column(Text)
    affected_years = Column(JSONB)
    prevalence = Column(String(50), comment="Very Common, Common, Occasional, Rare")
    detailed_description = Column(Text)
    root_cause = Column(Text)
    diagnosis_procedure = Column(Text)
    solution = Column(Text)
    repair_procedure_reference = Column(UUID(as_uuid=True), ForeignKey("repair_procedures.procedure_id"))
    parts_typically_needed = Column(JSONB)
    estimated_repair_cost = Column(String(100))
    prevention_tips = Column(Text)
    related_dtc_codes = Column(JSONB)
    related_tsb_numbers = Column(JSONB)
    community_reports = Column(Integer, default=0, comment="Number of user reports")
    verified = Column(Boolean, default=False)
    upvotes = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    vehicle = relationship("Vehicle", back_populates="common_problems")
    repair_procedure = relationship("RepairProcedure")

    def __repr__(self):
        return f"<CommonProblem {self.problem_title}>"
