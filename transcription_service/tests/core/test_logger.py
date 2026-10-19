import importlib
import logging

import app.core.config
import app.core.logger
from app.core.config import settings
from app.core.logger import LOGGING_CONFIG, setup_logging


def test_logging_config_dictionary_structure():
    """
    Verify the configuration dictionary contains the required formatters,
    handlers, and logger configurations.
    """
    assert LOGGING_CONFIG["version"] == 1
    assert LOGGING_CONFIG["disable_existing_loggers"] is False

    assert "formatters" in LOGGING_CONFIG
    assert "standard" in LOGGING_CONFIG["formatters"]
    assert "json" in LOGGING_CONFIG["formatters"]

    # Handlers configuration
    assert "console" in LOGGING_CONFIG["handlers"]
    console_handler = LOGGING_CONFIG["handlers"]["console"]
    assert console_handler["class"] == "logging.StreamHandler"
    assert console_handler["stream"] == "ext://sys.stdout"
    assert console_handler["formatter"] == "standard"

    # Ensure loggers are explicitly managed
    assert "" in LOGGING_CONFIG["loggers"]
    assert LOGGING_CONFIG["loggers"][""]["handlers"] == ["console"]
    assert "uvicorn.error" in LOGGING_CONFIG["loggers"]
    assert LOGGING_CONFIG["loggers"]["uvicorn.error"]["level"] == "INFO"
    assert "uvicorn.access" in LOGGING_CONFIG["loggers"]
    assert LOGGING_CONFIG["loggers"]["uvicorn.access"]["handlers"] == ["console"]
    assert LOGGING_CONFIG["loggers"]["uvicorn.access"]["level"] == "INFO"
    assert LOGGING_CONFIG["loggers"]["uvicorn.access"]["propagate"] is False


def test_logging_config_non_development_formatter(monkeypatch):
    """
    Verify that non-development environments (e.g. 'production', 'ci', 'staging')
    configure the JSON formatter for console logging.
    """
    for env in ("production", "ci", "staging"):
        monkeypatch.setattr(app.core.config.settings, "ENVIRONMENT", env)
        importlib.reload(app.core.logger)
        assert (
            app.core.logger.LOGGING_CONFIG["handlers"]["console"]["formatter"] == "json"
        )

    # Reset back to development
    monkeypatch.setattr(app.core.config.settings, "ENVIRONMENT", "development")
    importlib.reload(app.core.logger)
    assert (
        app.core.logger.LOGGING_CONFIG["handlers"]["console"]["formatter"] == "standard"
    )


def test_logging_config_uninterned_string_comparison(monkeypatch):
    """
    Verify that the environment check evaluates equality rather than identity.
    """
    uninterned_dev = "".join(["develop", "ment"])
    monkeypatch.setattr(app.core.config.settings, "ENVIRONMENT", uninterned_dev)
    importlib.reload(app.core.logger)
    assert (
        app.core.logger.LOGGING_CONFIG["handlers"]["console"]["formatter"] == "standard"
    )

    # Reset back
    monkeypatch.setattr(app.core.config.settings, "ENVIRONMENT", "development")
    importlib.reload(app.core.logger)


def test_setup_logging_applies_root_configuration():
    """
    Verify that setup_logging() attaches handlers to the root logger
    and applies the dynamic log level defined in the Pydantic settings.
    """
    setup_logging()
    root_logger = logging.getLogger()

    # Verify at least one handler (e.g., StreamHandler) is attached
    assert len(root_logger.handlers) > 0

    # Verify the global log level matches the environment configuration
    expected_level = logging.getLevelName(settings.LOG_LEVEL.upper())
    assert root_logger.level == expected_level


def test_application_logging_output(caplog):
    """
    Verify that application loggers can successfully emit messages
    and that the pytest capture fixture intercepts them at the correct severity.
    """
    setup_logging()
    logging.root.addHandler(caplog.handler)

    # Create a dummy logger to simulate application execution
    test_logger = logging.getLogger("app.test")
    test_message = "This is a critical system failure test."

    # Use caplog to capture output strictly at the ERROR level and above
    with caplog.at_level(logging.ERROR):
        test_logger.error(test_message)
        test_logger.debug("This hidden debug message should not be captured.")

    # Assert the error message was captured
    assert test_message in caplog.text
    assert caplog.records[0].levelname == "ERROR"
    assert caplog.records[0].name == "app.test"

    # Assert the debug message was successfully filtered out
    assert "hidden debug message" not in caplog.text
