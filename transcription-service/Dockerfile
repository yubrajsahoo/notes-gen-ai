# ==============================================================================
# Dockerfile for Transcription Service (FastAPI + FFmpeg + Faster-Whisper)
# ==============================================================================
FROM python:3.11-slim-bookworm

# Set Python & Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=8082 \
    HOST=0.0.0.0 \
    HF_HOME=/app/models_cache

# Set Working Directory
WORKDIR /app

# Install system dependencies:
# - ffmpeg: Required for video container demuxing & 16kHz PCM audio extraction
# - curl: Required for container health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root system user and prepare model cache directory
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser \
    && mkdir -p /app/models_cache \
    && chown -R appuser:appuser /app

# Copy dependency specifications first to leverage Docker layer caching
COPY requirements.txt .

# Install Python production dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application source code & configurations
COPY app/ ./app/
COPY main.py pyproject.toml ./

# Ensure correct file permissions for non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user for security
USER appuser

# Expose microservice HTTP & WebSocket port
EXPOSE 8082

# Define Container Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8082/health || exit 1

# Start FastAPI application via Uvicorn ASGI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8082"]
