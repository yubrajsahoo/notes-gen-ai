from pathlib import Path

import pytest
from pydantic import ValidationError

from transcription_service.core.config import Settings, settings


def test_default_settings():
    """Test that Settings initializes with expected default values."""
    config = Settings()
    assert config.PROJECT_NAME == "Transcription API"
    assert config.HOST == "localhost"
    assert config.PORT == 8000
    assert config.RELOAD is True
    assert config.DEBUG is True
    assert config.CORS_ORIGINS == ["*"]


def test_getattr_case_insensitive_access():
    """Test accessing attributes in lowercase or mixed case via __getattr__."""
    config = Settings()
    assert config.project_name == config.PROJECT_NAME
    assert config.host == config.HOST
    assert config.port == config.PORT
    assert config.reload == config.RELOAD
    assert config.debug == config.DEBUG
    assert config.cors_origins == config.CORS_ORIGINS
    assert config.Project_Name == config.PROJECT_NAME


def test_getattr_non_existent_attribute_raises():
    """Test that accessing a non-existent attribute raises AttributeError."""
    config = Settings()
    with pytest.raises(AttributeError):
        _ = config.non_existent_attribute

    with pytest.raises(AttributeError):
        _ = config.NON_EXISTENT_ATTRIBUTE


def test_settings_environment_variable_override(monkeypatch: pytest.MonkeyPatch):
    """Test that environment variables override default settings."""
    monkeypatch.setenv("PROJECT_NAME", "Custom Transcription API")
    monkeypatch.setenv("HOST", "0.0.0.0")
    monkeypatch.setenv("PORT", "9000")
    monkeypatch.setenv("RELOAD", "false")
    monkeypatch.setenv("DEBUG", "false")
    monkeypatch.setenv(
        "CORS_ORIGINS", '["http://localhost:3000", "https://app.example.com"]'
    )

    config = Settings()
    assert config.PROJECT_NAME == "Custom Transcription API"
    assert config.HOST == "0.0.0.0"
    assert config.PORT == 9000
    assert config.RELOAD is False
    assert config.DEBUG is False
    assert config.CORS_ORIGINS == [
        "http://localhost:3000",
        "https://app.example.com",
    ]
    assert config.project_name == "Custom Transcription API"
    assert config.port == 9000


def test_settings_from_env_file(tmp_path: Path):
    """Test loading settings from a custom .env file."""
    env_content = (
        'PROJECT_NAME="File API"\n'
        'HOST="192.168.1.10"\n'
        "PORT=8080\n"
        "RELOAD=false\n"
        "DEBUG=false\n"
        "CORS_ORIGINS='[\"http://test.com\"]'\n"
    )
    env_file = tmp_path / ".env"
    env_file.write_text(env_content, encoding="utf-8")

    config = Settings(_env_file=str(env_file))
    assert config.PROJECT_NAME == "File API"
    assert config.HOST == "192.168.1.10"
    assert config.PORT == 8080
    assert config.RELOAD is False
    assert config.DEBUG is False
    assert config.CORS_ORIGINS == ["http://test.com"]


def test_settings_validation_error():
    """Test that invalid types for settings raise a ValidationError."""
    with pytest.raises(ValidationError):
        Settings(PORT="not-an-int")


def test_global_settings_instance():
    """Test that the global settings instance is created properly."""
    assert isinstance(settings, Settings)
    assert settings.PROJECT_NAME == "Transcription API"
