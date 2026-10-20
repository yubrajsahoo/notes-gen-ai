import logging

import uvicorn
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logger import setup_logging


def create_app() -> FastAPI:
    logger.info(
        f"Starting FastApi {settings.PROJECT_NAME} (v{settings.VERSION}) "
        f"in {settings.ENVIRONMENT} mode."
    )

    application = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
    # Versioned API endpoints (e.g., /api/v1/...)
    application.include_router(router=api_router, prefix=settings.API_PREFIX)

    return application


setup_logging()
logger = logging.getLogger(__name__)
app = create_app()


def start() -> None:
    """Run application via uvicorn programmatically."""
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
    )


if __name__ == "__main__":  # pragma: no cover, no mutate
    start()
