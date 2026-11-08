import logging

import uvicorn
from fastapi import FastAPI

from transcription_service.core.config import settings
from transcription_service.core.logger import setup_logging
from transcription_service.core.middle_ware import setup_middleware
from transcription_service.routes.router import api_router

# Logging setup
setup_logging()

# Create a logger specifically for the main file
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)

setup_middleware(app)

# Include API routes
app.include_router(api_router)

# Include API v1 routes

# Run the application
if __name__ == "__main__":
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}...")
    uvicorn.run(
        "transcription_service.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
