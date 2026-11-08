import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from transcription_service.core import middle_ware
from transcription_service.core.middle_ware import setup_middleware


def test_setup_middleware_registers_cors():
    """Test that setup_middleware registers CORSMiddleware with expected options."""
    app = FastAPI()
    setup_middleware(app)

    assert len(app.user_middleware) == 1
    middleware = app.user_middleware[0]
    assert middleware.cls is CORSMiddleware
    assert middleware.kwargs["allow_origins"] == middle_ware.settings.CORS_ORIGINS
    assert middleware.kwargs["allow_credentials"] is True
    assert middleware.kwargs["allow_methods"] == ["*"]
    assert middleware.kwargs["allow_headers"] == ["*"]


def test_cors_preflight_and_headers():
    """Test CORS preflight OPTIONS and normal GET requests with default settings."""
    app = FastAPI()

    @app.get("/test")
    def sample_endpoint():
        return {"status": "ok"}

    setup_middleware(app)
    client = TestClient(app)

    # Preflight OPTIONS request
    preflight_response = client.options(
        "/test",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert preflight_response.status_code == 200
    assert (
        preflight_response.headers.get("access-control-allow-origin")
        == "http://localhost:3000"
    )
    assert preflight_response.headers.get("access-control-allow-credentials") == "true"

    # Standard GET request with Origin
    get_response = client.get(
        "/test",
        headers={"Origin": "http://localhost:3000"},
    )
    assert get_response.status_code == 200
    assert (
        get_response.headers.get("access-control-allow-origin")
        == "http://localhost:3000"
    )


def test_cors_with_restricted_origins(monkeypatch: pytest.MonkeyPatch):
    """Test CORS handling when specific origins are configured."""
    monkeypatch.setattr(
        middle_ware.settings, "CORS_ORIGINS", ["https://trusted.example.com"]
    )

    app = FastAPI()

    @app.get("/test")
    def sample_endpoint():
        return {"status": "ok"}

    setup_middleware(app)
    client = TestClient(app)

    # Request from allowed origin
    allowed_response = client.get(
        "/test",
        headers={"Origin": "https://trusted.example.com"},
    )
    assert allowed_response.status_code == 200
    assert (
        allowed_response.headers.get("access-control-allow-origin")
        == "https://trusted.example.com"
    )

    # Request from untrusted origin
    untrusted_response = client.get(
        "/test",
        headers={"Origin": "https://untrusted.example.com"},
    )
    assert untrusted_response.status_code == 200
    assert "access-control-allow-origin" not in untrusted_response.headers
