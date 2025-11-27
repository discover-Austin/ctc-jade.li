"""
Tests for VIN decoder endpoint.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_validate_vin_valid():
    """Test VIN validation with a valid VIN."""
    # Using a valid VIN checksum
    valid_vin = "1HGBH41JXMN109186"  # Honda VIN with valid check digit

    response = client.get(f"/api/v1/vin/validate/{valid_vin}")
    assert response.status_code == 200
    data = response.json()
    assert data["vin"] == valid_vin
    assert data["valid"] == True
    assert "manufacturer_code" in data


def test_validate_vin_invalid_length():
    """Test VIN validation with invalid length."""
    invalid_vin = "1HGBH41"  # Too short

    response = client.get(f"/api/v1/vin/validate/{invalid_vin}")
    assert response.status_code == 400
    assert "17 characters" in response.json()["detail"]


def test_validate_vin_invalid_characters():
    """Test VIN validation with invalid characters (I, O, Q)."""
    invalid_vin = "1HGBH41JXMN109IOQ"  # Contains I, O, Q

    response = client.get(f"/api/v1/vin/validate/{invalid_vin}")
    assert response.status_code == 400
    assert "cannot contain" in response.json()["detail"]


def test_vin_year_extraction():
    """Test that VIN validation extracts year correctly."""
    vin_2020 = "1HGBH41JXLN109186"  # L = 2020

    response = client.get(f"/api/v1/vin/validate/{vin_2020}")
    assert response.status_code == 200
    data = response.json()
    assert data["year"] == 2020


def test_vin_decode_request_validation():
    """Test VIN decode request validation."""
    # Test with empty VIN
    response = client.post("/api/v1/vin/decode", json={"vin": ""})
    assert response.status_code == 422

    # Test with short VIN
    response = client.post("/api/v1/vin/decode", json={"vin": "SHORT"})
    assert response.status_code == 422

    # Test with VIN containing invalid chars
    response = client.post("/api/v1/vin/decode", json={"vin": "1HGBH41JXMN109IOQ"})
    assert response.status_code == 422
