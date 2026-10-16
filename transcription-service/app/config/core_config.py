import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Service Configuration
SERVICE_NAME = os.getenv("SERVICE_NAME", "transcription-service")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8082"))
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")
WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
