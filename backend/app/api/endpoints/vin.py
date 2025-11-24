"""
VIN decoder API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import aiohttp
import re

from app.db.base import get_db
from app.schemas.vehicle import VINDecodeRequest, VINDecodeResponse
from app.core.config import settings

router = APIRouter()


def validate_vin(vin: str) -> bool:
    """
    Validate VIN using check digit algorithm (ISO 3779).

    Args:
        vin: Vehicle Identification Number (17 characters)

    Returns:
        bool: True if VIN is valid, False otherwise
    """
    if len(vin) != 17:
        return False

    # VIN transliteration table
    transliteration = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9,
        'S': 2, 'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9
    }

    weights = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]

    vin = vin.upper()
    sum_value = 0

    for i, char in enumerate(vin):
        if char.isdigit():
            value = int(char)
        else:
            value = transliteration.get(char, 0)
        sum_value += value * weights[i]

    check_digit = sum_value % 11
    if check_digit == 10:
        check_digit = 'X'
    else:
        check_digit = str(check_digit)

    return vin[8] == check_digit


async def query_nhtsa_vin_decoder(vin: str) -> dict:
    """
    Query NHTSA VIN decoder API.

    Args:
        vin: Vehicle Identification Number

    Returns:
        dict: Decoded VIN information
    """
    url = f"{settings.NHTSA_API_BASE_URL}/vehicles/DecodeVinValues/{vin}?format=json"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=500, detail="Failed to decode VIN from NHTSA API")

            data = await response.json()

            if data.get("Results") and len(data["Results"]) > 0:
                result = data["Results"][0]

                # Extract relevant fields
                return {
                    "vin": vin,
                    "year": int(result.get("ModelYear", 0)),
                    "make": result.get("Make", ""),
                    "model": result.get("Model", ""),
                    "trim": result.get("Trim", ""),
                    "engine": result.get("EngineModel", ""),
                    "transmission": result.get("TransmissionStyle", ""),
                    "body_style": result.get("BodyClass", ""),
                    "drive_type": result.get("DriveType", ""),
                    "manufacturer": result.get("Manufacturer", ""),
                    "plant_city": result.get("PlantCity", ""),
                    "plant_country": result.get("PlantCountry", ""),
                    "vehicle_type": result.get("VehicleType", ""),
                }
            else:
                raise HTTPException(status_code=404, detail="VIN not found in NHTSA database")


@router.post("/decode", response_model=VINDecodeResponse)
async def decode_vin(
    request: VINDecodeRequest,
    db: Session = Depends(get_db)
):
    """
    Decode VIN and return vehicle specifications.

    This endpoint validates the VIN using the ISO 3779 check digit algorithm,
    then queries the NHTSA VIN decoder API for detailed vehicle information.

    - **vin**: 17-character Vehicle Identification Number

    Returns detailed vehicle information including:
    - Year, make, model, trim
    - Engine and transmission type
    - Body style and drive type
    - Manufacturing information
    """
    vin = request.vin.upper()

    # Validate VIN format
    if not validate_vin(vin):
        raise HTTPException(status_code=400, detail="Invalid VIN - check digit validation failed")

    # Query NHTSA API for VIN decoding
    try:
        vin_data = await query_nhtsa_vin_decoder(vin)
        return VINDecodeResponse(**vin_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error decoding VIN: {str(e)}")


@router.get("/validate/{vin}")
async def validate_vin_endpoint(vin: str):
    """
    Validate a VIN without full decoding.

    This endpoint performs a quick validation using the ISO 3779 check digit algorithm.

    - **vin**: 17-character Vehicle Identification Number

    Returns:
    - **valid**: Boolean indicating if VIN is valid
    - **vin**: The validated VIN
    - **year**: Extracted model year from VIN position
    - **manufacturer_code**: World Manufacturer Identifier (positions 1-3)
    """
    vin = vin.upper()

    if len(vin) != 17:
        raise HTTPException(status_code=400, detail="VIN must be exactly 17 characters")

    # Check for invalid characters
    invalid_chars = {'I', 'O', 'Q'}
    if any(char in vin for char in invalid_chars):
        raise HTTPException(status_code=400, detail="VIN cannot contain I, O, or Q")

    is_valid = validate_vin(vin)

    # Extract year code (position 10)
    year_codes = {
        'A': 2010, 'B': 2011, 'C': 2012, 'D': 2013, 'E': 2014, 'F': 2015,
        'G': 2016, 'H': 2017, 'J': 2018, 'K': 2019, 'L': 2020, 'M': 2021,
        'N': 2022, 'P': 2023, 'R': 2024, 'S': 2025, 'T': 2026, 'V': 2027,
        'W': 2028, 'X': 2029, 'Y': 2030,
        '1': 2001, '2': 2002, '3': 2003, '4': 2004, '5': 2005,
        '6': 2006, '7': 2007, '8': 2008, '9': 2009
    }

    year_char = vin[9]
    year = year_codes.get(year_char, 0)

    return {
        "valid": is_valid,
        "vin": vin,
        "year": year,
        "manufacturer_code": vin[:3],
        "vehicle_descriptor": vin[3:9],
        "check_digit": vin[8],
        "model_year": vin[9],
        "plant_code": vin[10],
        "serial_number": vin[11:17]
    }
