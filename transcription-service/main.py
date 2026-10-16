from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.health import health_router
from app.config.core_config import (
    HOST,
    PORT,
    SERVICE_NAME,
    WHISPER_COMPUTE_TYPE,
    WHISPER_DEVICE,
    WHISPER_MODEL_SIZE,
)
from app.config.log_config import log


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI startup and shutdown events.
    Used to load the Faster-Whisper model and initialize RabbitMQ connections.
    """
    log.info(f"Starting {SERVICE_NAME} on {HOST}:{PORT}...")
    log.info(
        f"Whisper Config -> Model: {WHISPER_MODEL_SIZE}, "
        f"Device: {WHISPER_DEVICE}, Compute Type: {WHISPER_COMPUTE_TYPE}"
    )
    # TODO: Initialize Faster-Whisper model & RabbitMQ connection pool here
    yield
    # TODO: Close RabbitMQ connections and clean up resources here
    log.info(f"Shutting down {SERVICE_NAME}...")


# Initialize FastAPI Application
app = FastAPI(
    title="Notes-Gen-AI Transcription Service",
    description=(
        "Real-time audio/video speech-to-text microservice "
        "using FastAPI, FFmpeg, and Faster-Whisper."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for React UI (Port 3000) & API Gateway (Port 8080)[cite: 1, 3]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
