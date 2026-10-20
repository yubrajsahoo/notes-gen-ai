from fastapi import APIRouter

from app.core.config import settings

actuator_router = APIRouter()


@actuator_router.get(
    "", summary="API Information", description="Get information about the API"
)
@actuator_router.get("/", include_in_schema=False)
@actuator_router.get(
    "/health", summary="Health Status", description="Get the health status of the API"
)
async def actuators():
    return {
        "status": "ok",
        "message": "API is healthy and running.",
        "actuators": {
            "health": f"{settings.API_PREFIX}/actuators/health",
            "docs": "/docs",
            "redoc": "/redoc",
            "appDocs": "/docs",
            "appRedoc": "/redoc",
        },
    }
