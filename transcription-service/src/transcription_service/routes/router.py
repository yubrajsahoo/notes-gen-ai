from fastapi import APIRouter

from transcription_service.routes.common import health

api_router = APIRouter()

#include routers
api_router.include_router(health.router)