"""
Database seeding script with sample vehicle data.

This script populates the database with sample vehicles, repair procedures,
diagnostic codes, and other data for testing and development.
"""
import sys
from pathlib import Path
from decimal import Decimal
from datetime import date, datetime
import uuid

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base import SessionLocal
from app.models.vehicle import Vehicle, Engine, Transmission, SuspensionSystem, BrakeSystem
from app.models.electrical import ElectricalSystem, BatterySpec, AlternatorSpec
from app.models.repair import RepairProcedure, TorqueSpec, MaintenanceSchedule
from app.models.diagnostic import DiagnosticCode, OBD2PID, LiveDataRange
from app.models.technical import TechnicalBulletin, Recall, CommonProblem
from app.models.fluid import FluidSpec
from app.models.wheel_tire import WheelTireSpec

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_sample_toyota_camry_2020(db):
    """Create a complete 2020 Toyota Camry with all subsystems."""
    logger.info("Creating 2020 Toyota Camry...")

    # Create vehicle
    camry = Vehicle(
        vehicle_id=uuid.uuid4(),
        vin_pattern="4T1B11HK*L",
        year=2020,
        make="Toyota",
        model="Camry",
        trim="SE",
        body_style="Sedan",
        drive_type="FWD",
        transmission_type="8-Speed Automatic",
        engine_config="2.5L I4",
        production_start=date(2019, 7, 1),
        production_end=date(2021, 6, 30),
        market_region="North America",
        platform_code="XV70",
        data_verified=True,
        verification_source="Factory Service Manual"
    )
    db.add(camry)

    # Create engine
    engine = Engine(
        engine_id=uuid.uuid4(),
        vehicle_id=camry.vehicle_id,
        engine_code="A25A-FKS",
        displacement_liters=Decimal("2.5"),
        displacement_cc=2487,
        cylinders=4,
        configuration="Inline-4",
        aspiration="Naturally Aspirated",
        fuel_system="Direct Injection",
        horsepower=203,
        horsepower_rpm=6600,
        torque_lb_ft=184,
        torque_rpm=5000,
        compression_ratio=Decimal("13.0"),
        bore_mm=Decimal("87.5"),
        stroke_mm=Decimal("103.4"),
        firing_order="1-3-4-2",
        valve_train="DOHC 16-valve",
        emissions_standard="LEV3 ULEV70",
        hybrid_system=False
    )
    db.add(engine)

    # Create transmission
    transmission = Transmission(
        transmission_id=uuid.uuid4(),
        vehicle_id=camry.vehicle_id,
        transmission_code="U881F",
        type="Automatic",
        speeds=8,
        final_drive_ratio=Decimal("4.158"),
        gear_ratios={
            "1st": "5.172",
            "2nd": "3.109",
            "3rd": "2.074",
            "4th": "1.567",
            "5th": "1.262",
            "6th": "1.000",
            "7th": "0.824",
            "8th": "0.692",
            "Reverse": "4.595"
        },
        fluid_type="Toyota WS (World Standard) ATF",
        fluid_capacity_quarts=Decimal("8.5"),
        service_interval_miles=60000,
        manufacturer="Aisin"
    )
    db.add(transmission)

    # Create electrical system
    electrical = ElectricalSystem(
        electrical_id=uuid.uuid4(),
        vehicle_id=camry.vehicle_id,
        battery_voltage=12,
        battery_cca=520,
        battery_rc=100,
        battery_group_size="35",
        alternator_output_amps=130,
        alternator_voltage=Decimal("13.5"),
        starter_type="Gear Reduction",
        charging_system_specs={"voltage_range": "13.5-14.8V"}
    )
    db.add(electrical)

    # Create wheel/tire spec
    wheel_tire = WheelTireSpec(
        spec_id=uuid.uuid4(),
        vehicle_id=camry.vehicle_id,
        tire_size_front="235/45R18",
        tire_size_rear="235/45R18",
        wheel_diameter_inches=18,
        wheel_width_inches=Decimal("8.0"),
        wheel_offset_mm=45,
        bolt_pattern="5x114.3",
        center_bore_mm=Decimal("60.1"),
        lug_nut_torque_lb_ft=76,
        tire_pressure_front_psi=35,
        tire_pressure_rear_psi=35,
        tpms_type="Direct",
        wheel_material="Aluminum Alloy"
    )
    db.add(wheel_tire)

    # Create fluid specs
    fluids = [
        FluidSpec(
            fluid_id=uuid.uuid4(),
            vehicle_id=camry.vehicle_id,
            fluid_type="Engine Oil",
            specification="0W-20 API SN",
            capacity_quarts=Decimal("4.6"),
            change_interval_miles=10000,
            change_interval_months=12,
            oem_part_number="00279-0WQTE-01"
        ),
        FluidSpec(
            fluid_id=uuid.uuid4(),
            vehicle_id=camry.vehicle_id,
            fluid_type="Coolant",
            specification="Toyota Super Long Life Coolant",
            capacity_quarts=Decimal("7.4"),
            change_interval_miles=100000,
            change_interval_months=120,
            oem_part_number="00272-1LLAC-01"
        ),
        FluidSpec(
            fluid_id=uuid.uuid4(),
            vehicle_id=camry.vehicle_id,
            fluid_type="Brake Fluid",
            specification="DOT 3",
            capacity_quarts=Decimal("0.7"),
            change_interval_miles=30000,
            change_interval_months=36,
            oem_part_number="00475-1BF03"
        )
    ]
    for fluid in fluids:
        db.add(fluid)

    # Create sample repair procedure
    oil_change = RepairProcedure(
        procedure_id=uuid.uuid4(),
        vehicle_id=camry.vehicle_id,
        system_category="Engine",
        subsystem="Lubrication",
        procedure_name="Engine Oil and Filter Change",
        difficulty_level="Beginner",
        estimated_time_hours=Decimal("0.5"),
        labor_time_oem_hours=Decimal("0.3"),
        special_tools_required=["Oil filter wrench", "Drain pan", "Funnel"],
        safety_precautions="Ensure engine is cool. Wear safety glasses and gloves.",
        prerequisites="Vehicle on level ground, parking brake applied",
        procedure_steps=[
            {"step": 1, "description": "Warm up engine to operating temperature, then turn off"},
            {"step": 2, "description": "Raise vehicle and support securely on jack stands"},
            {"step": 3, "description": "Place drain pan under oil pan"},
            {"step": 4, "description": "Remove drain plug and allow oil to drain completely"},
            {"step": 5, "description": "Replace drain plug washer and reinstall drain plug"},
            {"step": 6, "description": "Remove oil filter using filter wrench"},
            {"step": 7, "description": "Clean filter mounting surface"},
            {"step": 8, "description": "Apply thin film of oil to new filter gasket"},
            {"step": 9, "description": "Install new filter, hand-tighten plus 3/4 turn"},
            {"step": 10, "description": "Lower vehicle"},
            {"step": 11, "description": "Add 4.4 quarts of 0W-20 oil through filler cap"},
            {"step": 12, "description": "Start engine and check for leaks"},
            {"step": 13, "description": "Turn off engine, wait 5 minutes, check oil level"},
            {"step": 14, "description": "Add oil as needed to reach full mark"},
            {"step": 15, "description": "Reset maintenance reminder system"}
        ],
        torque_specifications=[
            {"component": "Oil drain plug", "torque_lb_ft": 30, "torque_nm": 41}
        ],
        parts_required=[
            {"part_number": "04152-YZZA1", "description": "Oil filter", "quantity": 1},
            {"part_number": "90430-12031", "description": "Drain plug gasket", "quantity": 1}
        ],
        consumables_required=[
            {"item": "0W-20 Engine Oil", "quantity": "4.6 quarts"}
        ],
        tips_and_tricks="Dispose of used oil properly at recycling center. Record mileage for next service.",
        revision_number=1,
        revision_date=date.today(),
        verified_by="ASE Master Technician",
        source="Toyota Factory Service Manual"
    )
    db.add(oil_change)

    # Create diagnostic codes
    dtc_codes = [
        DiagnosticCode(
            dtc_id=uuid.uuid4(),
            vehicle_id=camry.vehicle_id,
            code="P0300",
            code_type="Powertrain",
            system="Engine",
            description="Random/Multiple Cylinder Misfire Detected",
            symptoms="Check engine light, rough idle, loss of power, poor fuel economy",
            possible_causes=[
                "Faulty spark plugs or ignition coils",
                "Vacuum leaks",
                "Low fuel pressure",
                "Clogged fuel injectors",
                "Engine mechanical issues",
                "Bad fuel"
            ],
            diagnostic_steps=[
                {"step": 1, "description": "Verify code with OBD-II scanner"},
                {"step": 2, "description": "Check for additional codes (P030X for specific cylinders)"},
                {"step": 3, "description": "Inspect spark plugs and ignition coils"},
                {"step": 4, "description": "Check fuel pressure (43-55 PSI at idle)"},
                {"step": 5, "description": "Perform compression test if mechanical issues suspected"},
                {"step": 6, "description": "Inspect for vacuum leaks"},
                {"step": 7, "description": "Test fuel injectors"}
            ],
            severity="Important",
            emission_related=True,
            drive_cycle_requirements="Two consecutive drive cycles with fault present"
        ),
        DiagnosticCode(
            dtc_id=uuid.uuid4(),
            vehicle_id=camry.vehicle_id,
            code="P0420",
            code_type="Powertrain",
            system="Emissions",
            description="Catalyst System Efficiency Below Threshold (Bank 1)",
            symptoms="Check engine light, possible slight reduction in fuel economy",
            possible_causes=[
                "Failed catalytic converter",
                "Faulty oxygen sensor",
                "Engine oil contamination in exhaust",
                "Exhaust leak before catalytic converter"
            ],
            diagnostic_steps=[
                {"step": 1, "description": "Verify code and check for exhaust leaks"},
                {"step": 2, "description": "Monitor O2 sensor data (Bank 1 Sensor 1 vs Sensor 2)"},
                {"step": 3, "description": "Check for oil consumption issues"},
                {"step": 4, "description": "Inspect catalytic converter for damage"},
                {"step": 5, "description": "Replace catalytic converter if efficiency confirmed low"}
            ],
            severity="Important",
            emission_related=True
        )
    ]
    for dtc in dtc_codes:
        db.add(dtc)

    # Create torque specifications
    torque_specs = [
        TorqueSpec(
            torque_id=uuid.uuid4(),
            vehicle_id=camry.vehicle_id,
            component_name="Cylinder head bolts",
            system_category="Engine",
            fastener_description="M10 bolts, 10-point socket required",
            torque_lb_ft=None,  # Multi-step torque
            torque_nm=None,
            torque_sequence="Center outward in spiral pattern",
            additional_procedures="Step 1: 27 lb-ft, Step 2: +90°, Step 3: +90°",
            thread_locker_required=False,
            lubrication_required=True,
            lubrication_type="Engine oil on threads",
            reusability="Replace bolts - stretch type, one-time use only"
        ),
        TorqueSpec(
            torque_id=uuid.uuid4(),
            vehicle_id=camry.vehicle_id,
            component_name="Wheel lug nuts",
            system_category="Chassis",
            fastener_description="21mm hex",
            torque_lb_ft=76,
            torque_nm=103,
            torque_sequence="Star pattern",
            thread_locker_required=False,
            lubrication_required=False,
            reusability="Inspect threads, replace if damaged"
        ),
        TorqueSpec(
            torque_id=uuid.uuid4(),
            vehicle_id=camry.vehicle_id,
            component_name="Spark plugs",
            system_category="Engine",
            fastener_description="16mm hex, iridium-tipped",
            torque_lb_ft=18,
            torque_nm=25,
            thread_locker_required=False,
            lubrication_required=True,
            lubrication_type="Anti-seize on threads",
            reusability="Replace at 120,000 miles"
        )
    ]
    for spec in torque_specs:
        db.add(spec)

    # Create maintenance schedule
    maintenance_items = [
        MaintenanceSchedule(
            schedule_id=uuid.uuid4(),
            vehicle_id=camry.vehicle_id,
            service_item="Engine Oil and Filter Change",
            interval_miles=10000,
            interval_months=12,
            interval_type="Normal",
            description="Replace engine oil and filter",
            parts_required=[{"part": "Oil filter", "part_number": "04152-YZZA1"}],
            fluids_required=[{"fluid": "0W-20 Engine Oil", "quantity": "4.6 quarts"}],
            estimated_cost_range="$40-80",
            priority="Critical"
        ),
        MaintenanceSchedule(
            schedule_id=uuid.uuid4(),
            vehicle_id=camry.vehicle_id,
            service_item="Tire Rotation",
            interval_miles=5000,
            interval_months=6,
            interval_type="Normal",
            description="Rotate tires and check pressure",
            estimated_cost_range="$20-40",
            priority="Important"
        ),
        MaintenanceSchedule(
            schedule_id=uuid.uuid4(),
            vehicle_id=camry.vehicle_id,
            service_item="Cabin Air Filter",
            interval_miles=15000,
            interval_months=12,
            interval_type="Normal",
            description="Replace cabin air filter",
            parts_required=[{"part": "Cabin air filter", "part_number": "87139-02090"}],
            estimated_cost_range="$15-30",
            priority="Minor"
        )
    ]
    for item in maintenance_items:
        db.add(item)

    # Create common problem
    common_problem = CommonProblem(
        problem_id=uuid.uuid4(),
        vehicle_id=camry.vehicle_id,
        problem_title="Excessive Oil Consumption",
        problem_category="Engine",
        symptoms="Low oil warning light, engine running rough, blue smoke from exhaust",
        prevalence="Moderate",
        detailed_description="Some 2018-2020 Camry models with 2.5L engine experience higher than normal oil consumption, requiring oil top-ups between changes.",
        root_cause="Piston ring design allows oil to pass into combustion chamber",
        diagnosis_procedure="Monitor oil level every 1000 miles. Consumption >1 quart per 1000 miles is excessive.",
        solution="Toyota TSB EG-022-19 covers this issue. Dealer may perform piston and ring replacement under warranty extension.",
        estimated_repair_cost="Covered under warranty extension, otherwise $2000-3500",
        community_reports=45,
        verified=True,
        upvotes=38
    )
    db.add(common_problem)

    logger.info("✅ 2020 Toyota Camry created successfully with all subsystems!")
    return camry


def create_sample_honda_accord_2019(db):
    """Create a 2019 Honda Accord."""
    logger.info("Creating 2019 Honda Accord...")

    accord = Vehicle(
        vehicle_id=uuid.uuid4(),
        vin_pattern="1HGCV1F*K",
        year=2019,
        make="Honda",
        model="Accord",
        trim="Sport",
        body_style="Sedan",
        drive_type="FWD",
        transmission_type="CVT",
        engine_config="1.5L Turbo I4",
        production_start=date(2018, 8, 1),
        production_end=date(2020, 7, 31),
        market_region="North America",
        platform_code="CV",
        data_verified=True,
        verification_source="Honda Service Manual"
    )
    db.add(accord)

    engine = Engine(
        engine_id=uuid.uuid4(),
        vehicle_id=accord.vehicle_id,
        engine_code="L15B7",
        displacement_liters=Decimal("1.5"),
        displacement_cc=1498,
        cylinders=4,
        configuration="Inline-4",
        aspiration="Turbocharged",
        fuel_system="Direct Injection",
        horsepower=192,
        horsepower_rpm=5500,
        torque_lb_ft=192,
        torque_rpm=1600,
        compression_ratio=Decimal("10.3"),
        valve_train="DOHC 16-valve VTEC",
        emissions_standard="LEV3 ULEV125"
    )
    db.add(engine)

    transmission = Transmission(
        transmission_id=uuid.uuid4(),
        vehicle_id=accord.vehicle_id,
        transmission_code="CVT",
        type="Continuously Variable",
        final_drive_ratio=Decimal("4.684"),
        fluid_type="Honda CVT Fluid HCF-2",
        fluid_capacity_quarts=Decimal("3.4"),
        service_interval_miles=50000,
        manufacturer="Honda"
    )
    db.add(transmission)

    logger.info("✅ 2019 Honda Accord created successfully!")
    return accord


def create_sample_ford_f150_2021(db):
    """Create a 2021 Ford F-150."""
    logger.info("Creating 2021 Ford F-150...")

    f150 = Vehicle(
        vehicle_id=uuid.uuid4(),
        vin_pattern="1FTFW1E*M",
        year=2021,
        make="Ford",
        model="F-150",
        trim="XLT",
        body_style="Crew Cab Pickup",
        drive_type="4WD",
        transmission_type="10-Speed Automatic",
        engine_config="3.5L V6 EcoBoost",
        production_start=date(2020, 9, 1),
        production_end=None,
        market_region="North America",
        platform_code="P558",
        data_verified=True,
        verification_source="Ford Service Manual"
    )
    db.add(f150)

    engine = Engine(
        engine_id=uuid.uuid4(),
        vehicle_id=f150.vehicle_id,
        engine_code="3.5L EcoBoost V6",
        displacement_liters=Decimal("3.5"),
        displacement_cc=3496,
        cylinders=6,
        configuration="V6",
        aspiration="Twin-Turbocharged",
        fuel_system="Direct Injection",
        horsepower=400,
        horsepower_rpm=6000,
        torque_lb_ft=500,
        torque_rpm=3100,
        compression_ratio=Decimal("10.5"),
        valve_train="DOHC 24-valve Ti-VCT"
    )
    db.add(engine)

    transmission = Transmission(
        transmission_id=uuid.uuid4(),
        vehicle_id=f150.vehicle_id,
        transmission_code="10R80",
        type="Automatic",
        speeds=10,
        final_drive_ratio=Decimal("3.55"),
        fluid_type="Mercon ULV",
        fluid_capacity_quarts=Decimal("13.9"),
        service_interval_miles=150000,
        manufacturer="Ford"
    )
    db.add(transmission)

    logger.info("✅ 2021 Ford F-150 created successfully!")
    return f150


def seed_database():
    """Main seeding function."""
    logger.info("Starting database seeding...")

    db = SessionLocal()

    try:
        # Check if data already exists
        existing_count = db.query(Vehicle).count()
        if existing_count > 0:
            logger.warning(f"⚠️  Database already contains {existing_count} vehicles.")
            response = input("Do you want to add more sample data? (yes/no): ")
            if response.lower() != "yes":
                logger.info("Seeding cancelled.")
                return

        # Create sample vehicles
        camry = create_sample_toyota_camry_2020(db)
        accord = create_sample_honda_accord_2019(db)
        f150 = create_sample_ford_f150_2021(db)

        # Commit all changes
        db.commit()

        logger.info("=" * 60)
        logger.info("✅ Database seeding completed successfully!")
        logger.info(f"Total vehicles in database: {db.query(Vehicle).count()}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
