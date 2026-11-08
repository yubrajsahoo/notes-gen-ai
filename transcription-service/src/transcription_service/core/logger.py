import logging
import sys

from transcription_service.core.config import settings


def setup_logging():
    """Configures basic logging for the FastAPI application."""

    # 1. Define the log format
    # Example: 2023-10-25 14:30:00 - routes - INFO - User uploaded file
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 2. Create a handler to output logs to the console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # 3. Get the root logger and set the base level based on your .env
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Prevent duplicate logs by clearing existing handlers
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(console_handler)

    # 4. (Optional but recommended) Override Uvicorn's default loggers
    # so they match your custom format
    for logger_name in ("uvicorn.access", "uvicorn.error"):
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers = [console_handler]
        uvicorn_logger.propagate = False
