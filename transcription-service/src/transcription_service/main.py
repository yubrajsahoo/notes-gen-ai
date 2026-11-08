import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from transcription_service.core.config import settings
from transcription_service.routes.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)

# --- Add the CORS Middleware here ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # The list we defined in config.py
    allow_credentials=True,  # Allows cookies and authentication headers
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include API routes
app.include_router(api_router)

# Include API v1 routes

# run the application
if __name__ == "__main__":
    uvicorn.run(
        "transcription_service.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
