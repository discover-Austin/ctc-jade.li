"""
Database initialization script.

This script creates all database tables and initializes the schema.
Run this before seeding data.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base import Base, engine
from app.models.vehicle import (
    Vehicle, Engine, Transmission, SuspensionSystem, BrakeSystem
)
from app.models.electrical import ElectricalSystem, BatterySpec, AlternatorSpec, StarterSpec
from app.models.repair import RepairProcedure, TorqueSpec, MaintenanceSchedule
from app.models.diagnostic import DiagnosticCode, OBD2PID, LiveDataRange
from app.models.technical import TechnicalBulletin, Recall, CommonProblem
from app.models.fluid import FluidSpec
from app.models.parts import Part, PartInterchange
from app.models.wheel_tire import WheelTireSpec

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """Initialize the database by creating all tables."""
    logger.info("Creating database tables...")

    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")

        # Print created tables
        logger.info(f"Created {len(Base.metadata.tables)} tables:")
        for table_name in sorted(Base.metadata.tables.keys()):
            logger.info(f"  - {table_name}")

    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        raise


def drop_all():
    """Drop all database tables. USE WITH CAUTION!"""
    logger.warning("⚠️  Dropping all database tables...")
    response = input("Are you sure you want to drop all tables? (yes/no): ")

    if response.lower() == "yes":
        try:
            Base.metadata.drop_all(bind=engine)
            logger.info("✅ All tables dropped successfully!")
        except Exception as e:
            logger.error(f"❌ Error dropping tables: {e}")
            raise
    else:
        logger.info("Cancelled. No tables were dropped.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database initialization script")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all tables before creating (WARNING: destroys all data)"
    )

    args = parser.parse_args()

    if args.drop:
        drop_all()

    init_db()
