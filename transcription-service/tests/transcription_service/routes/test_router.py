from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

from transcription_service.routes.common import health
from transcription_service.routes.router import api_router


def test_api_router_instance():
    """Test that api_router is an instance of APIRouter."""
    assert isinstance(api_router, APIRouter)


def test_api_router_includes_health_router():
    """Test that health router is registered within api_router."""
    included_routers = [getattr(r, "original_router", None) for r in api_router.routes]
    assert health.router in included_routers


def test_api_router_requests():
    """Test requests through an app mounting api_router."""
    app = FastAPI()
    app.include_router(api_router)
    client = TestClient(app)

    root_response = client.get("/")
    assert root_response.status_code == 200
    assert root_response.json() == {"status": "healthy"}

    health_response = client.get("/health")
    assert health_response.status_code == 200
    assert health_response.json() == {"status": "healthy"}
