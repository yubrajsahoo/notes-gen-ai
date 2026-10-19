import logging

import uvicorn
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logger import setup_logging

# Allows running the script directly
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False,
    )


setup_logging()
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    logger.info(
        f"Starting FastApi {settings.PROJECT_NAME} (v{settings.VERSION}) "
        f"in {settings.ENVIRONMENT} mode."
    )

    application = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
    application.include_router(router=api_router, prefix=settings.API_PREFIX)

    return application


app = create_app()