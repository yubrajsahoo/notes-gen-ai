from fastapi import APIRouter

health_router = APIRouter(tags=["Health"])


@health_router.get("/health")
def health_check():
    """
    Health check endpoint to verify that the API is running.
    """
    return {"status": "healthy", "service": "transcription-service"}
