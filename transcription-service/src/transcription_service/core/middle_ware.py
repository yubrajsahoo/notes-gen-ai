# transcription_service/core/middle_ware.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from transcription_service.core.config import settings


def setup_middleware(app: FastAPI) -> None:
    """Registers all middleware for the FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
