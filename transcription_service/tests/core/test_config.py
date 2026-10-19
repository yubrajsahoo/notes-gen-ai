import logging
import os
import sys

import pytest

from app.core.config import Settings

logger = logging.getLogger(__name__)


def test_default_settings():
    """
    Test that the default settings are loaded correctly.
    """
    settings = Settings()

    assert settings.PROJECT_NAME == "transcription_service"
    assert settings.LOG_LEVEL == "INFO"
    assert settings.ENVIRONMENT == "development"
    assert settings.API_PREFIX == "/api/v1"


def test_environment_variable_override():
    """
    Test that environment variables override the default settings.
    """
    os.environ["ENVIRONMENT"] = "production"
    os.environ["LOG_LEVEL"] = "WARNING"

    settings = Settings()

    assert settings.ENVIRONMENT == "production"
    assert settings.LOG_LEVEL == "WARNING"

    del os.environ["ENVIRONMENT"]
    del os.environ["LOG_LEVEL"]


def test_metadata_extraction():
    """
    Test that the metadata extraction methods return the correct values.
    """
    settings = Settings()

    assert settings.PROJECT_NAME == "transcription_service"
    assert isinstance(settings.VERSION, str)
    assert len(settings.VERSION) > 0


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Windows environment variables are case-insensitive",
)
def test_case_sensitivity():
    """
    Test that the settings are case-sensitive.
    """
    os.environ["environment"] = "staging"  # Lowercase key
    settings = Settings()

    # The lowercase key should not override the default value
    assert settings.ENVIRONMENT == "development"

    del os.environ["environment"]


def test_model_config_attributes():
    """
    Test that model_config specifies case sensitivity, extra ignore,
    and the proper env_file.
    """
    assert Settings.model_config.get("case_sensitive") is True
    assert Settings.model_config.get("extra") == "ignore"
    assert Settings.model_config.get("env_file") == ".env"
    assert Settings.model_config.get("env_file_encoding") == "utf-8"
