"""
Tests for vehicle API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from app.main import app
from app.db.base import Base, get_db
from app.models.vehicle import Vehicle, Engine, Transmission

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_vehicle(test_db):
    """Create a sample vehicle for testing."""
    db = TestingSessionLocal()

    vehicle = Vehicle(
        vehicle_id=uuid4(),
        year=2020,
        make="Toyota",
        model="Camry",
        trim="SE",
        body_style="Sedan",
        drive_type="FWD",
        engine_config="2.5L I4",
        data_verified=True
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    yield vehicle

    db.close()


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "version" in response.json()


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Vehicle Repair Database API" in response.json()["message"]


def test_search_vehicles_no_filters(test_db):
    """Test vehicle search with no filters returns error."""
    response = client.get("/api/v1/vehicles/search")
    assert response.status_code == 404


def test_search_vehicles_by_year(sample_vehicle):
    """Test searching vehicles by year."""
    response = client.get("/api/v1/vehicles/search?year=2020")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["year"] == 2020


def test_search_vehicles_by_make(sample_vehicle):
    """Test searching vehicles by make."""
    response = client.get("/api/v1/vehicles/search?make=Toyota")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "Toyota" in data[0]["make"]


def test_search_vehicles_by_model(sample_vehicle):
    """Test searching vehicles by model."""
    response = client.get("/api/v1/vehicles/search?model=Camry")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "Camry" in data[0]["model"]


def test_search_vehicles_combined_filters(sample_vehicle):
    """Test searching with multiple filters."""
    response = client.get("/api/v1/vehicles/search?year=2020&make=Toyota&model=Camry")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["year"] == 2020
    assert "Toyota" in data[0]["make"]
    assert "Camry" in data[0]["model"]


def test_get_vehicle_by_id(sample_vehicle):
    """Test getting a specific vehicle by ID."""
    response = client.get(f"/api/v1/vehicles/{sample_vehicle.vehicle_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["vehicle_id"] == str(sample_vehicle.vehicle_id)
    assert data["year"] == 2020
    assert data["make"] == "Toyota"


def test_get_vehicle_not_found():
    """Test getting a vehicle that doesn't exist."""
    fake_id = uuid4()
    response = client.get(f"/api/v1/vehicles/{fake_id}")
    assert response.status_code == 404


def test_pagination(test_db):
    """Test pagination parameters."""
    # Create multiple vehicles
    db = TestingSessionLocal()
    for i in range(15):
        vehicle = Vehicle(
            vehicle_id=uuid4(),
            year=2020 + (i % 3),
            make="Toyota",
            model=f"Model_{i}",
            data_verified=True
        )
        db.add(vehicle)
    db.commit()
    db.close()

    # Test limit
    response = client.get("/api/v1/vehicles/search?year=2020&limit=5")
    assert response.status_code == 200
    assert len(response.json()) <= 5

    # Test offset
    response = client.get("/api/v1/vehicles/search?make=Toyota&offset=10")
    assert response.status_code == 200


def test_invalid_year_filter():
    """Test searching with invalid year."""
    response = client.get("/api/v1/vehicles/search?year=abc")
    assert response.status_code == 422  # Validation error
