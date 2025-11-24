"""
Pydantic schemas for vehicle-related requests and responses.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from uuid import UUID
from decimal import Decimal


class VehicleBase(BaseModel):
    """Base vehicle schema."""

    year: int = Field(..., ge=2014, le=2030, description="Model year")
    make: str = Field(..., max_length=100)
    model: str = Field(..., max_length=100)
    trim: Optional[str] = Field(None, max_length=100)
    body_style: Optional[str] = None
    drive_type: Optional[str] = None
    transmission_type: Optional[str] = None
    engine_config: Optional[str] = None


class VehicleCreate(VehicleBase):
    """Schema for creating a new vehicle."""

    vin_pattern: Optional[str] = Field(None, max_length=17)
    production_start: Optional[date] = None
    production_end: Optional[date] = None
    market_region: Optional[str] = None
    platform_code: Optional[str] = None


class VehicleResponse(VehicleBase):
    """Schema for vehicle response."""

    vehicle_id: UUID
    vin_pattern: Optional[str] = None
    production_start: Optional[date] = None
    production_end: Optional[date] = None
    market_region: Optional[str] = None
    platform_code: Optional[str] = None
    data_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class VehicleSearchRequest(BaseModel):
    """Schema for vehicle search request."""

    year: Optional[int] = Field(None, ge=2014, le=2030)
    make: Optional[str] = None
    model: Optional[str] = None
    engine: Optional[str] = None
    vin: Optional[str] = Field(None, min_length=17, max_length=17)

    @validator('vin')
    def validate_vin(cls, v):
        if v:
            v = v.upper()
            if len(v) != 17:
                raise ValueError('VIN must be exactly 17 characters')
            # Remove invalid characters
            invalid_chars = {'I', 'O', 'Q'}
            if any(char in v for char in invalid_chars):
                raise ValueError('VIN cannot contain I, O, or Q')
        return v


class EngineResponse(BaseModel):
    """Schema for engine response."""

    engine_id: UUID
    vehicle_id: UUID
    engine_code: str
    displacement_liters: Optional[Decimal] = None
    displacement_cc: Optional[int] = None
    cylinders: Optional[int] = None
    configuration: Optional[str] = None
    aspiration: Optional[str] = None
    fuel_system: Optional[str] = None
    horsepower: Optional[int] = None
    horsepower_rpm: Optional[int] = None
    torque_lb_ft: Optional[int] = None
    torque_rpm: Optional[int] = None
    compression_ratio: Optional[Decimal] = None
    bore_mm: Optional[Decimal] = None
    stroke_mm: Optional[Decimal] = None
    firing_order: Optional[str] = None
    valve_train: Optional[str] = None
    camshaft_specs: Optional[Dict[str, Any]] = None
    emissions_standard: Optional[str] = None
    hybrid_system: bool = False
    hybrid_type: Optional[str] = None
    battery_kwh: Optional[Decimal] = None
    electric_motor_hp: Optional[int] = None
    electric_range_miles: Optional[int] = None

    class Config:
        from_attributes = True


class TransmissionResponse(BaseModel):
    """Schema for transmission response."""

    transmission_id: UUID
    vehicle_id: UUID
    transmission_code: Optional[str] = None
    type: Optional[str] = None
    speeds: Optional[int] = None
    final_drive_ratio: Optional[Decimal] = None
    gear_ratios: Optional[Dict[str, Any]] = None
    torque_converter_specs: Optional[Dict[str, Any]] = None
    transfer_case_ratios: Optional[Dict[str, Any]] = None
    fluid_type: Optional[str] = None
    fluid_capacity_quarts: Optional[Decimal] = None
    service_interval_miles: Optional[int] = None
    manufacturer: Optional[str] = None

    class Config:
        from_attributes = True


class VehicleDetailResponse(VehicleResponse):
    """Detailed vehicle response including all related data."""

    engines: List[EngineResponse] = []
    transmissions: List[TransmissionResponse] = []

    class Config:
        from_attributes = True


class VINDecodeRequest(BaseModel):
    """Schema for VIN decode request."""

    vin: str = Field(..., min_length=17, max_length=17)

    @validator('vin')
    def validate_vin(cls, v):
        v = v.upper()
        if len(v) != 17:
            raise ValueError('VIN must be exactly 17 characters')
        # Remove invalid characters
        invalid_chars = {'I', 'O', 'Q'}
        if any(char in v for char in invalid_chars):
            raise ValueError('VIN cannot contain I, O, or Q')
        return v


class VINDecodeResponse(BaseModel):
    """Schema for VIN decode response."""

    vin: str
    year: int
    make: str
    model: str
    trim: Optional[str] = None
    engine: Optional[str] = None
    transmission: Optional[str] = None
    body_style: Optional[str] = None
    drive_type: Optional[str] = None
    manufacturer: Optional[str] = None
    plant_city: Optional[str] = None
    plant_country: Optional[str] = None
    vehicle_type: Optional[str] = None
