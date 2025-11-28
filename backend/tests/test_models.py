"""
Tests for database models.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from uuid import uuid4
from datetime import date

from app.db.base import Base
from app.models.vehicle import Vehicle, Engine, Transmission
from app.models.repair import RepairProcedure, TorqueSpec
from app.models.diagnostic import DiagnosticCode
from app.models.technical import TechnicalBulletin, Recall, CommonProblem

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_models.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create test database session."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_create_vehicle(db_session):
    """Test creating a vehicle."""
    vehicle = Vehicle(
        vehicle_id=uuid4(),
        year=2020,
        make="Toyota",
        model="Camry",
        trim="SE",
        body_style="Sedan",
        drive_type="FWD",
        data_verified=True
    )

    db_session.add(vehicle)
    db_session.commit()

    assert vehicle.vehicle_id is not None
    assert vehicle.year == 2020
    assert vehicle.make == "Toyota"
    assert str(vehicle) == "<Vehicle 2020 Toyota Camry>"


def test_create_engine_with_vehicle(db_session):
    """Test creating an engine associated with a vehicle."""
    vehicle = Vehicle(
        vehicle_id=uuid4(),
        year=2020,
        make="Toyota",
        model="Camry",
        data_verified=True
    )
    db_session.add(vehicle)
    db_session.commit()

    engine_obj = Engine(
        engine_id=uuid4(),
        vehicle_id=vehicle.vehicle_id,
        engine_code="2AR-FE",
        displacement_liters=Decimal("2.5"),
        displacement_cc=2494,
        cylinders=4,
        configuration="Inline-4",
        horsepower=203,
        torque_lb_ft=184
    )

    db_session.add(engine_obj)
    db_session.commit()

    assert engine_obj.vehicle_id == vehicle.vehicle_id
    assert len(vehicle.engines) == 1
    assert vehicle.engines[0].engine_code == "2AR-FE"


def test_create_repair_procedure(db_session):
    """Test creating a repair procedure."""
    vehicle = Vehicle(
        vehicle_id=uuid4(),
        year=2020,
        make="Toyota",
        model="Camry",
        data_verified=True
    )
    db_session.add(vehicle)
    db_session.commit()

    procedure = RepairProcedure(
        procedure_id=uuid4(),
        vehicle_id=vehicle.vehicle_id,
        system_category="Engine",
        procedure_name="Oil Change",
        difficulty_level="Beginner",
        estimated_time_hours=Decimal("0.5"),
        procedure_steps=[
            {"step": 1, "description": "Drain oil"},
            {"step": 2, "description": "Replace filter"}
        ],
        verified_by="Technician"
    )

    db_session.add(procedure)
    db_session.commit()

    assert procedure.procedure_id is not None
    assert procedure.system_category == "Engine"
    assert len(procedure.procedure_steps) == 2


def test_create_diagnostic_code(db_session):
    """Test creating a diagnostic code."""
    vehicle = Vehicle(
        vehicle_id=uuid4(),
        year=2020,
        make="Toyota",
        model="Camry",
        data_verified=True
    )
    db_session.add(vehicle)
    db_session.commit()

    dtc = DiagnosticCode(
        dtc_id=uuid4(),
        vehicle_id=vehicle.vehicle_id,
        code="P0300",
        code_type="Powertrain",
        system="Engine",
        description="Random/Multiple Cylinder Misfire",
        possible_causes=["Spark plugs", "Ignition coils"],
        severity="Important",
        emission_related=True
    )

    db_session.add(dtc)
    db_session.commit()

    assert dtc.code == "P0300"
    assert dtc.emission_related == True
    assert len(dtc.possible_causes) == 2


def test_create_torque_spec(db_session):
    """Test creating torque specifications."""
    vehicle = Vehicle(
        vehicle_id=uuid4(),
        year=2020,
        make="Toyota",
        model="Camry",
        data_verified=True
    )
    db_session.add(vehicle)
    db_session.commit()

    torque_spec = TorqueSpec(
        torque_id=uuid4(),
        vehicle_id=vehicle.vehicle_id,
        component_name="Cylinder head bolts",
        system_category="Engine",
        torque_lb_ft=70,
        torque_nm=95,
        torque_sequence="Center outward"
    )

    db_session.add(torque_spec)
    db_session.commit()

    assert torque_spec.torque_lb_ft == 70
    assert torque_spec.torque_nm == 95


def test_vehicle_relationships(db_session):
    """Test that vehicle relationships work correctly."""
    vehicle = Vehicle(
        vehicle_id=uuid4(),
        year=2020,
        make="Toyota",
        model="Camry",
        data_verified=True
    )
    db_session.add(vehicle)
    db_session.commit()

    # Add engine
    engine_obj = Engine(
        engine_id=uuid4(),
        vehicle_id=vehicle.vehicle_id,
        engine_code="2AR-FE",
        displacement_liters=Decimal("2.5")
    )
    db_session.add(engine_obj)

    # Add transmission
    trans = Transmission(
        transmission_id=uuid4(),
        vehicle_id=vehicle.vehicle_id,
        transmission_code="U660E",
        type="Automatic",
        speeds=6
    )
    db_session.add(trans)

    # Add DTC
    dtc = DiagnosticCode(
        dtc_id=uuid4(),
        vehicle_id=vehicle.vehicle_id,
        code="P0420",
        description="Catalyst Efficiency Low",
        emission_related=True
    )
    db_session.add(dtc)

    db_session.commit()

    # Verify relationships
    db_session.refresh(vehicle)
    assert len(vehicle.engines) == 1
    assert len(vehicle.transmissions) == 1
    assert len(vehicle.diagnostic_codes) == 1


def test_cascade_delete(db_session):
    """Test that cascade delete works for vehicle relationships."""
    vehicle = Vehicle(
        vehicle_id=uuid4(),
        year=2020,
        make="Toyota",
        model="Camry",
        data_verified=True
    )
    db_session.add(vehicle)
    db_session.commit()

    # Add related data
    engine_obj = Engine(
        engine_id=uuid4(),
        vehicle_id=vehicle.vehicle_id,
        engine_code="2AR-FE"
    )
    db_session.add(engine_obj)
    db_session.commit()

    # Delete vehicle
    db_session.delete(vehicle)
    db_session.commit()

    # Verify engine was also deleted (cascade)
    remaining_engines = db_session.query(Engine).filter(
        Engine.vehicle_id == vehicle.vehicle_id
    ).all()
    assert len(remaining_engines) == 0
