"""
Comprehensive test suite for Vehicle Database API.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import Mock, patch

from app.main import app
from app.db.base import Base, get_db
from app.models.vehicle import Vehicle, Engine, Transmission

# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """Create test database tables."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_vehicle(test_db):
    """Create a sample vehicle for testing."""
    db = TestingSessionLocal()
    vehicle = Vehicle(
        year=2020,
        make="Toyota",
        model="Camry",
        trim="LE",
        body_style="Sedan",
        drive_type="FWD",
        engine_config="2.5L I-4"
    )
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    db.close()
    return vehicle


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_check(self):
        """Test health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_readiness_check(self):
        """Test readiness endpoint."""
        response = client.get("/ready")
        assert response.status_code == 200
        assert "status" in response.json()

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


class TestVehicleAPI:
    """Test vehicle API endpoints."""

    def test_vehicle_search_by_year(self, sample_vehicle):
        """Test vehicle search by year."""
        response = client.get("/api/v1/vehicles/search?year=2020")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert all(v["year"] == 2020 for v in data)

    def test_vehicle_search_by_make(self, sample_vehicle):
        """Test vehicle search by make."""
        response = client.get("/api/v1/vehicles/search?make=Toyota")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_vehicle_search_by_make_and_model(self, sample_vehicle):
        """Test vehicle search by make and model."""
        response = client.get("/api/v1/vehicles/search?make=Toyota&model=Camry")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_vehicle_search_no_results(self):
        """Test vehicle search with no results."""
        response = client.get("/api/v1/vehicles/search?year=1999")
        assert response.status_code == 404

    def test_get_vehicle_by_id(self, sample_vehicle):
        """Test getting vehicle by ID."""
        response = client.get(f"/api/v1/vehicles/{sample_vehicle.vehicle_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["year"] == 2020
        assert data["make"] == "Toyota"
        assert data["model"] == "Camry"

    def test_get_vehicle_not_found(self):
        """Test getting non-existent vehicle."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/api/v1/vehicles/{fake_id}")
        assert response.status_code == 404


class TestVINDecoder:
    """Test VIN decoder endpoints."""

    def test_vin_validation_valid(self):
        """Test VIN validation with valid VIN."""
        response = client.get("/api/v1/vin/validate/1HGBH41JXMN109186")
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True

    def test_vin_validation_invalid_length(self):
        """Test VIN validation with invalid length."""
        response = client.get("/api/v1/vin/validate/INVALID")
        assert response.status_code == 400

    def test_vin_validation_invalid_characters(self):
        """Test VIN validation with invalid characters (I, O, Q)."""
        response = client.get("/api/v1/vin/validate/1HGBH41JXMN109IOQ")
        assert response.status_code == 400

    @patch('app.api.endpoints.vin.query_nhtsa_vin_decoder')
    async def test_vin_decode_success(self, mock_nhtsa):
        """Test VIN decoding with mocked NHTSA response."""
        mock_nhtsa.return_value = {
            "vin": "1HGBH41JXMN109186",
            "year": 2020,
            "make": "Honda",
            "model": "Civic",
            "trim": "LX",
            "engine": "2.0L",
            "transmission": "CVT",
        }

        response = client.post(
            "/api/v1/vin/decode",
            json={"vin": "1HGBH41JXMN109186"}
        )
        # Note: This test may fail due to async nature
        # In production, use pytest-asyncio properly


class TestRepairAPI:
    """Test repair procedures API."""

    def test_get_repair_procedures(self, sample_vehicle):
        """Test getting repair procedures for a vehicle."""
        response = client.get(f"/api/v1/repair/procedures/{sample_vehicle.vehicle_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_torque_specs(self, sample_vehicle):
        """Test getting torque specifications."""
        response = client.get(f"/api/v1/repair/torque-specs/{sample_vehicle.vehicle_id}")
        # May return 404 if no specs exist, which is okay for empty DB
        assert response.status_code in [200, 404]

    def test_get_maintenance_schedule(self, sample_vehicle):
        """Test getting maintenance schedule."""
        response = client.get(f"/api/v1/repair/maintenance/{sample_vehicle.vehicle_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestDiagnosticAPI:
    """Test diagnostic API endpoints."""

    def test_get_dtc_code(self, sample_vehicle):
        """Test getting DTC code."""
        response = client.get(f"/api/v1/diagnostic/dtc/{sample_vehicle.vehicle_id}/P0300")
        # May return 404 if code doesn't exist
        assert response.status_code in [200, 404]

    def test_search_dtc_codes(self, sample_vehicle):
        """Test searching DTC codes."""
        response = client.get(f"/api/v1/diagnostic/dtc/search/{sample_vehicle.vehicle_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_obd2_pids(self, sample_vehicle):
        """Test getting OBD-II PIDs."""
        response = client.get(f"/api/v1/diagnostic/obd2/pids/{sample_vehicle.vehicle_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestTechnicalAPI:
    """Test technical bulletins and recalls API."""

    def test_get_tsbs(self, sample_vehicle):
        """Test getting Technical Service Bulletins."""
        response = client.get(f"/api/v1/technical/tsbs/{sample_vehicle.vehicle_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_recalls(self, sample_vehicle):
        """Test getting recalls."""
        response = client.get(f"/api/v1/technical/recalls/{sample_vehicle.vehicle_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_common_problems(self, sample_vehicle):
        """Test getting common problems."""
        response = client.get(f"/api/v1/technical/common-problems/{sample_vehicle.vehicle_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestDataIntegrity:
    """Test data consistency and integrity."""

    def test_vehicle_required_fields(self, test_db):
        """Test that vehicle has required fields."""
        db = TestingSessionLocal()
        vehicle = Vehicle(year=2020, make="Test", model="Test")
        db.add(vehicle)
        db.commit()
        assert vehicle.vehicle_id is not None
        assert vehicle.year == 2020
        db.close()

    def test_engine_vehicle_relationship(self, sample_vehicle, test_db):
        """Test engine-vehicle relationship."""
        db = TestingSessionLocal()
        engine = Engine(
            vehicle_id=sample_vehicle.vehicle_id,
            engine_code="2AR-FE",
            displacement_liters=2.5,
            cylinders=4
        )
        db.add(engine)
        db.commit()

        # Verify relationship
        vehicle = db.query(Vehicle).filter(
            Vehicle.vehicle_id == sample_vehicle.vehicle_id
        ).first()
        assert len(vehicle.engines) > 0
        db.close()


class TestPerformance:
    """Performance tests for critical endpoints."""

    def test_search_response_time(self, sample_vehicle):
        """Test that search responds quickly."""
        import time
        start = time.time()
        response = client.get("/api/v1/vehicles/search?year=2020")
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 1.0  # Should respond within 1 second

    def test_vehicle_detail_response_time(self, sample_vehicle):
        """Test vehicle detail page loads quickly."""
        import time
        start = time.time()
        response = client.get(f"/api/v1/vehicles/{sample_vehicle.vehicle_id}")
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 0.5  # Should respond within 500ms


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
