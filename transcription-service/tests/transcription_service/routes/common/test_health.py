import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from transcription_service.routes.common.health import health_check, router


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_health_check_root_endpoint(client: TestClient):
    """Test GET / returns healthy status."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_health_check_health_endpoint(client: TestClient):
    """Test GET /health returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_health_check_method_not_allowed(client: TestClient):
    """Test POST to /health returns 405 Method Not Allowed."""
    response = client.post("/health")
    assert response.status_code == 405


@pytest.mark.anyio
async def test_health_check_direct_call():
    """Test direct invocation of the health_check coroutine."""
    result = await health_check()
    assert result == {"status": "healthy"}
