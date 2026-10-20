from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app, start


@pytest.fixture
def client():
    """
    Test client fixture using FastAPI's TestClient against the application.
    """
    return TestClient(app)


def test_actuators_endpoint(client):
    """
    Verify that the actuators home endpoint is accessible at /actuators.
    """
    response = client.get(f"{settings.API_PREFIX}/actuators", follow_redirects=False)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "API is healthy and running."
    actuators = data["actuators"]
    assert actuators["health"] == f"{settings.API_PREFIX}/actuators/health"
    assert actuators["docs"] == "/docs"
    assert actuators["redoc"] == "/redoc"
    assert actuators["appDocs"] == "/docs"
    assert actuators["appRedoc"] == "/redoc"


def test_actuators_endpoint_with_trailing_slash(client):
    """
    Verify the actuator home endpoint does not redirect a trailing-slash request.
    """
    response = client.get(f"{settings.API_PREFIX}/actuators/", follow_redirects=False)
    assert response.status_code == 200
    assert (
        response.json()["actuators"]["health"]
        == f"{settings.API_PREFIX}/actuators/health"
    )


def test_actuator_trailing_slash_not_in_schema(client):
    """
    Verify that the trailing slash alias is excluded from the OpenAPI schema.
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    assert f"{settings.API_PREFIX}/actuators" in paths
    assert f"{settings.API_PREFIX}/actuators/" not in paths


def test_health_endpoint(client):
    """
    Verify that the health check endpoint returns status ok at /actuators/health.
    """
    response = client.get(f"{settings.API_PREFIX}/actuators/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "API is healthy and running."


def test_start_development(monkeypatch):
    """
    Verify start() launches uvicorn with reload enabled in development.
    """
    monkeypatch.setattr(settings, "ENVIRONMENT", "development")
    with patch("uvicorn.run") as mock_run:
        start()
        mock_run.assert_called_once_with(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
        )


def test_start_non_development(monkeypatch):
    """
    Verify start() launches uvicorn with reload disabled in
    non-development environments.
    """
    for env in ("production", "ci", "staging"):
        monkeypatch.setattr(settings, "ENVIRONMENT", env)
        with patch("uvicorn.run") as mock_run:
            start()
            mock_run.assert_called_once_with(
                "app.main:app",
                host="127.0.0.1",
                port=8000,
                reload=False,
            )


def test_start_uninterned_development(monkeypatch):
    """
    Verify start() evaluates string equality rather than identity.
    """
    uninterned_dev = "".join(["develop", "ment"])
    monkeypatch.setattr(settings, "ENVIRONMENT", uninterned_dev)
    with patch("uvicorn.run") as mock_run:
        start()
        mock_run.assert_called_once_with(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
        )
