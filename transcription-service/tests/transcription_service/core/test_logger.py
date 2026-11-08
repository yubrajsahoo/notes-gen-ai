import logging
import sys

import pytest

from transcription_service.core import logger
from transcription_service.core.logger import setup_logging


@pytest.fixture(autouse=True)
def restore_logging_state():
    """Preserves and restores logging configuration before and after each test."""
    root_logger = logging.getLogger()
    orig_level = root_logger.level
    orig_handlers = list(root_logger.handlers)

    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_error = logging.getLogger("uvicorn.error")
    orig_access_handlers = list(uvicorn_access.handlers)
    orig_access_propagate = uvicorn_access.propagate
    orig_error_handlers = list(uvicorn_error.handlers)
    orig_error_propagate = uvicorn_error.propagate

    yield

    root_logger.setLevel(orig_level)
    root_logger.handlers = orig_handlers

    uvicorn_access.handlers = orig_access_handlers
    uvicorn_access.propagate = orig_access_propagate
    uvicorn_error.handlers = orig_error_handlers
    uvicorn_error.propagate = orig_error_propagate


def test_setup_logging_debug_mode(monkeypatch: pytest.MonkeyPatch):
    """Test setup_logging configures root logger to DEBUG when DEBUG is True."""
    monkeypatch.setattr(logger.settings, "DEBUG", True)

    setup_logging()

    root_logger = logging.getLogger()
    assert root_logger.level == logging.DEBUG
    assert len(root_logger.handlers) == 1

    handler = root_logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert handler.stream == sys.stdout
    assert (
        handler.formatter._fmt == "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    assert handler.formatter.datefmt == "%Y-%m-%d %H:%M:%S"


def test_setup_logging_info_mode(monkeypatch: pytest.MonkeyPatch):
    """Test setup_logging configures root logger to INFO when DEBUG is False."""
    monkeypatch.setattr(logger.settings, "DEBUG", False)

    setup_logging()

    root_logger = logging.getLogger()
    assert root_logger.level == logging.INFO


def test_setup_logging_clears_existing_handlers():
    """Test that existing handlers on the root logger are cleared."""
    root_logger = logging.getLogger()
    root_logger.addHandler(logging.NullHandler())
    root_logger.addHandler(logging.NullHandler())
    assert len(root_logger.handlers) >= 2

    setup_logging()

    assert len(root_logger.handlers) == 1
    assert isinstance(root_logger.handlers[0], logging.StreamHandler)


def test_setup_logging_uvicorn_loggers():
    """Test uvicorn loggers are overridden with custom handler and propagate=False."""
    setup_logging()

    console_handler = logging.getLogger().handlers[0]

    for logger_name in ("uvicorn.access", "uvicorn.error"):
        uv_logger = logging.getLogger(logger_name)
        assert uv_logger.handlers == [console_handler]
        assert uv_logger.propagate is False


def test_logging_output_formatting(capsys: pytest.CaptureFixture):
    """Test logged messages adhere to the configured format and output to stdout."""
    setup_logging()

    test_logger = logging.getLogger("test_logger")
    test_logger.info("This is a test log message")

    captured = capsys.readouterr()
    assert " - test_logger - INFO - This is a test log message" in captured.out
