"""
Database models for the Vehicle Repair Database system.
"""
from .vehicle import Vehicle, Engine, Transmission, SuspensionSystem, BrakeSystem
from .electrical import ElectricalSystem, WiringDiagram, SensorSpecification
from .fluid import FluidSpecification, HVACSystem, FuelSystem
from .wheel_tire import WheelTireSpec
from .repair import RepairProcedure, TorqueSpec, MaintenanceSchedule
from .diagnostic import DiagnosticCode, OBD2PID, LiveDataRange
from .technical import TechnicalBulletin, Recall, CommonProblem
from .parts import PartsCatalog

__all__ = [
    "Vehicle",
    "Engine",
    "Transmission",
    "SuspensionSystem",
    "BrakeSystem",
    "ElectricalSystem",
    "WiringDiagram",
    "SensorSpecification",
    "FluidSpecification",
    "HVACSystem",
    "FuelSystem",
    "WheelTireSpec",
    "RepairProcedure",
    "TorqueSpec",
    "MaintenanceSchedule",
    "DiagnosticCode",
    "OBD2PID",
    "LiveDataRange",
    "TechnicalBulletin",
    "Recall",
    "CommonProblem",
    "PartsCatalog",
]
