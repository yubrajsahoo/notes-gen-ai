import runpy
import sys
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

from transcription_service.core.config import settings
from transcription_service.main import app


def test_app_instance_and_metadata():
    """Test that app is configured with expected metadata from settings."""
    assert isinstance(app, FastAPI)
    assert app.title == settings.PROJECT_NAME
    assert app.debug == settings.DEBUG


def test_app_middleware_registered():
    """Test that CORS middleware is registered on the FastAPI app."""
    middleware_classes = [m.cls for m in app.user_middleware]
    assert CORSMiddleware in middleware_classes


def test_app_endpoints():
    """Test that health check and openapi routes are mounted on app."""
    client = TestClient(app)

    root_res = client.get("/")
    assert root_res.status_code == 200
    assert root_res.json() == {"status": "healthy"}

    health_res = client.get("/health")
    assert health_res.status_code == 200
    assert health_res.json() == {"status": "healthy"}

    openapi_res = client.get("/openapi.json")
    assert openapi_res.status_code == 200
    assert openapi_res.json()["info"]["title"] == settings.PROJECT_NAME


def test_main_entrypoint(monkeypatch: pytest.MonkeyPatch):
    """Test __main__ script execution block runs uvicorn with configured settings."""
    mock_uvicorn_run = MagicMock()
    monkeypatch.setattr("uvicorn.run", mock_uvicorn_run)

    # Remove cached module from sys.modules so runpy runs fresh without warning
    saved_module = sys.modules.pop("transcription_service.main", None)
    try:
        runpy.run_module("transcription_service.main", run_name="__main__")
    finally:
        if saved_module is not None:
            sys.modules["transcription_service.main"] = saved_module

    mock_uvicorn_run.assert_called_once_with(
        "transcription_service.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
