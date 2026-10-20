from fastapi import APIRouter

from app.api.routes.actuators import actuator_router

api_router = APIRouter()

api_router.include_router(
    router=actuator_router, prefix="/actuators", tags=["Actuators"]
)
