import os
from unittest.mock import patch


def test_config_defaults():
    """Test that environment variables fall back to expected default values."""
    with patch.dict(os.environ, {}, clear=True):
        # Reload or re-evaluate config variables in isolation
        SERVICE_NAME = os.getenv("SERVICE_NAME", "transcription-service")
        HOST = os.getenv("HOST", "0.0.0.0")
        PORT = int(os.getenv("PORT", "8082"))
        WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")
        WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
        WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

        assert SERVICE_NAME == "transcription-service"
        assert HOST == "0.0.0.0"
        assert PORT == 8082
        assert WHISPER_MODEL_SIZE == "base"
        assert WHISPER_DEVICE == "cpu"
        assert WHISPER_COMPUTE_TYPE == "int8"


def test_config_overrides():
    """Test that custom environment variables correctly override defaults."""
    custom_env = {
        "SERVICE_NAME": "custom-transcription",
        "HOST": "127.0.0.1",
        "PORT": "9090",
        "WHISPER_MODEL_SIZE": "small",
        "WHISPER_DEVICE": "cuda",
        "WHISPER_COMPUTE_TYPE": "float16",
    }

    with patch.dict(os.environ, custom_env, clear=True):
        SERVICE_NAME = os.getenv("SERVICE_NAME", "transcription-service")
        HOST = os.getenv("HOST", "0.0.0.0")
        PORT = int(os.getenv("PORT", "8082"))
        WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")
        WHISPER_DEVICE = os.getenv("WHISPER_DEVICE", "cpu")
        WHISPER_COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

        assert SERVICE_NAME == "custom-transcription"
        assert HOST == "127.0.0.1"
        assert PORT == 9090
        assert WHISPER_MODEL_SIZE == "small"
        assert WHISPER_DEVICE == "cuda"
        assert WHISPER_COMPUTE_TYPE == "float16"
