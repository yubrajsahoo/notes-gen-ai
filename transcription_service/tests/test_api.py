import logging

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app, create_app


@pytest.fixture
def client():
    """
    Test client fixture using FastAPI's TestClient against the application.
    """
    return TestClient(app)


def test_app_instance():
    """
    Verify that the module-level app object is properly instantiated
    with configuration attributes loaded from settings.
    """
    assert isinstance(app, FastAPI)
    assert app.title == settings.PROJECT_NAME
    assert app.version == settings.VERSION


def test_create_app_factory():
    """
    Verify that the create_app factory produces a FastAPI instance
    configured with the project settings.
    """
    custom_app = create_app()
    assert isinstance(custom_app, FastAPI)
    assert custom_app.title == settings.PROJECT_NAME
    assert custom_app.version == settings.VERSION


def test_create_app_logs_startup(caplog):
    """
    Verify that invoking create_app emits an informative startup log message.
    """
    logging.root.addHandler(caplog.handler)
    expected_message = (
        f"Starting FastApi {settings.PROJECT_NAME} (v{settings.VERSION}) "
        f"in {settings.ENVIRONMENT} mode."
    )

    with caplog.at_level(logging.INFO):
        create_app()

    assert expected_message in caplog.text


def test_openapi_endpoint(client):
    """
    Verify that the OpenAPI JSON schema is generated and accessible.
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == settings.PROJECT_NAME
    assert schema["info"]["version"] == settings.VERSION


def test_docs_endpoint(client):
    """
    Verify that the Swagger UI documentation endpoint is accessible.
    """
    response = client.get("/docs")
    assert response.status_code == 200
