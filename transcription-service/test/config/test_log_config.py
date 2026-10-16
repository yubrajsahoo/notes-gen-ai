import logging

from app.config.log_config import log


def test_logger_configuration():
    """Test that the logger is correctly initialized with the expected name and log level."""
    assert isinstance(log, logging.Logger)
    assert log.name == "transcription-service"
    assert log.level <= logging.INFO


def test_log_output(caplog):
    """Test that the logger successfully records log messages."""
    with caplog.at_level(logging.INFO):
        log.info("Test log message for transcription service")

        assert "Test log message for transcription service" in caplog.text
