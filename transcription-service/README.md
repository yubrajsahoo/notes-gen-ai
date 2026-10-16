# Transcription Service (`transcription-service`)

The **Transcription Service** is a core Python microservice within the **Notes-Gen-AI** platform[cite: 1, 2]. Running on **Port 8082**[cite: 1, 2, 3], it ingests real-time audio and video chunks over WebSockets, extracts and normalizes the audio track using FFmpeg, performs speech-to-text transcription via Faster-Whisper, broadcasts live transcripts back to the React frontend (`note-gen-ui`), and publishes completion events to RabbitMQ[cite: 1, 2, 3].

---

## ⚡ Quick Start Commands (Run One by One)

### 1. Navigate to the Project Directory
```bash
cd E:\GitWork\notes-gen-ai\transcription-service
```

### 2. Create the Virtual Environment
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
**On Windows (CMD / PowerShell):**
```bash
venv\Scripts\activate
```

**On Linux / macOS / Git Bash:**
```bash
source venv/bin/activate
```

**(Optional) If PowerShell blocks script execution on Windows:**
```powershell
Set-ExecutionPolicy Unrestricted -Scope Process
```
```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies from `requirements.txt`
```bash
pip install -r requirements.txt
```

### 5. Start the FastAPI Server (Development Mode on Port 8082)
```bash
uvicorn main:app --host 0.0.0.0 --port 8082 --reload
```

---

## 📦 Step-by-Step Dependency Installation Commands

### 1. Install System-Level FFmpeg Binary
FFmpeg is required at the OS level to demux video containers and normalize audio to 16kHz mono PCM[cite: 1].

**Install FFmpeg on Windows (via Winget):**
```powershell
winget install Gyan.FFmpeg
```

**Install FFmpeg on Windows (via Chocolatey):**
```powershell
choco install ffmpeg -y
```

**Install FFmpeg on Ubuntu / Debian Linux:**
```bash
sudo apt update && sudo apt install -y ffmpeg
```

**Verify Python Installation:**
```bash
python --version
```

**Verify FFmpeg Installation:**
```bash
ffmpeg -version
```

### 2. Upgrade Pip & Packaging Tools
```bash
python -m pip install --upgrade pip setuptools wheel
```

### 3. Install Python Packages
**Install all packages from `requirements.txt`:**
```bash
pip install -r requirements.txt
```

**Or install core FastAPI & transcription packages manually[cite: 1, 2]:**
```bash
pip install fastapi uvicorn pydantic websockets faster-whisper ffmpeg-python numpy aio-pika python-dotenv
```

**(Optional) Install NVIDIA CUDA libraries if running Faster-Whisper on GPU[cite: 1]:**
```bash
pip install nvidia-cublas-cu12 nvidia-cudnn-cu12
```

**Verify installed Python packages:**
```bash
pip list
```

**Freeze currently installed package versions into `requirements.txt`:**
```bash
pip freeze > requirements.txt
```

---

## 🚀 Application Deployment Commands (Run One by One)

### Option 1: Local Development Deployment
**Run with Uvicorn (Auto-Reload enabled)[cite: 2]:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8082 --reload
```

**Run with FastAPI CLI (Development mode):**
```bash
fastapi dev main.py --host 0.0.0.0 --port 8082
```

---

### Option 2: Bare-Metal / VM Production Deployment
**Run Uvicorn with 4 Worker Processes (Windows / Linux):**
```bash
uvicorn main:app --host 0.0.0.0 --port 8082 --workers 4 --no-access-log
```

**Run with FastAPI CLI (Production mode):**
```bash
fastapi run main.py --host 0.0.0.0 --port 8082 --workers 4
```

**Install Gunicorn (Linux Production Servers only):**
```bash
pip install gunicorn
```

**Run Gunicorn with Uvicorn Workers (Linux Production Servers only):**
```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8082
```

---

### Option 3: Docker Container Deployment[cite: 3]

**1. Build the Docker Image:**
```bash
docker build -t notes-gen-ai/transcription-service:1.0.0 .
```

**2. Run the Docker Container on Port 8082:**
```bash
docker run -d --name transcription-service -p 8082:8082 --env-file .env notes-gen-ai/transcription-service:1.0.0
```

**3. View Live Container Logs:**
```bash
docker logs -f transcription-service
```

**4. Stop the Running Container:**
```bash
docker stop transcription-service
```

**5. Remove the Container:**
```bash
docker rm transcription-service
```

---

### Option 4: Docker Compose Deployment (Service + RabbitMQ)[cite: 1, 3]

**1. Build and Start All Services in Detached Mode:**
```bash
docker compose up -d --build
```

**2. Check Status of Running Containers:**
```bash
docker compose ps
```

**3. View Live Logs for Transcription Service:**
```bash
docker compose logs -f transcription-service
```

**4. Stop and Remove All Docker Compose Containers:**
```bash
docker compose down
```

---

### Option 5: Kubernetes (K8s) Cluster Deployment[cite: 3]

**1. Tag the Docker Image for Container Registry:**
```bash
docker tag notes-gen-ai/transcription-service:1.0.0 your-registry/transcription-service:1.0.0
```

**2. Push the Image to Container Registry:**
```bash
docker push your-registry/transcription-service:1.0.0
```

**3. Apply Kubernetes Deployment Manifest:**
```bash
kubectl apply -f k8s/deployment.yaml
```

**4. Apply Kubernetes Service Manifest:**
```bash
kubectl apply -f k8s/service.yaml
```

**5. Check Pod Status:**
```bash
kubectl get pods -l app=transcription-service
```

**6. Verify Deployment Rollout Status:**
```bash
kubectl rollout status deployment/transcription-service
```

**7. Stream Live Pod Logs:**
```bash
kubectl logs -l app=transcription-service -f
```

**8. Port-Forward Service to Local Port 8082:**
```bash
kubectl port-forward svc/transcription-service 8082:8082
```

---

## 🧪 Health Check, Testing & Environment Maintenance

**Check Service Health Endpoint[cite: 2]:**
```bash
curl http://localhost:8082/health
```

**Install `wscat` Globally (for WebSocket testing):**
```bash
npm install -g wscat
```

**Test Live WebSocket Endpoint (`/ws/transcribe`)[cite: 1, 2]:**
```bash
wscat -c ws://localhost:8082/ws/transcribe
```

**Deactivate the Python Virtual Environment:**
```bash
deactivate
```

---

## 🔍 Code Quality & Test Coverage

### ⚡ One-Click Automated Build & Verification Script (`build.bat`)
Runs the full 10-step build pipeline on Windows (syntax check, Ruff, Flake8, Black, isort, Mypy, Bandit, Pytest with coverage, FastAPI smoke test):
```cmd
build.bat
```
To install or re-sync all dependencies before building:
```cmd
build.bat --install
```

### 1. Install Development & Quality Dependencies
```bash
pip install -r requirements-dev.txt
```

### 2. Run Test Suite with Coverage
Runs pytest, measures test coverage on `app/`, enforces an 80% coverage threshold, and generates terminal and HTML reports:
```bash
pytest
```
Or run directly with explicit options:
```bash
pytest --cov=app --cov-report=term-missing --cov-report=html:coverage_html --cov-fail-under=80
```
View the generated HTML coverage report in browser:
```bash
# On Windows
start coverage_html/index.html
```

### 3. Run Code Quality Checks
**Fast Linter & Formatter Check (Ruff):**
```bash
ruff check .
```

**PEP 8 Compliance Check (Flake8):**
```bash
flake8
```

**Code Formatting Check (Black):**
```bash
black --check .
```
To auto-format files with Black:
```bash
black .
```

**Import Sorting Check (isort):**
```bash
isort --check-only .
```
To auto-sort imports with isort:
```bash
isort .
```

**Static Type Checking (mypy):**
```bash
mypy app
```

**Security Vulnerability Scan (Bandit):**
```bash
bandit -c pyproject.toml -r app
```

---

## 🏗️ Architecture & Internal Pipeline

Whether the user selects **Audio-Only** mode or **Audio + Video** mode in the frontend, this single module handles both inputs seamlessly because speech-to-text models strictly process audio tracks[cite: 1].

```text
                           ┌────────────────────────┐
                           │ WebSocket /ws/transcribe│
                           └───────────┬────────────┘
                                       │
                      Input Format Check / Media Header
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
       [ Audio Chunks ]                              [ Video Chunks ]
    (e.g., audio/webm; opus)                      (e.g., video/webm; vp8/vp9)
                │                                             │
                │                                             ▼
                │                                    ┌──────────────────┐
                │                                    │  FFmpeg Process  │
                │                                    │  (Strip Video /  │
                │                                    │   Extract PCM)   │
                │                                    └────────┬─────────┘
                │                                             │
                └──────────────────────┬──────────────────────┘
                                       ▼
                         [ Linear 16kHz PCM Audio ]
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │   Faster-Whisper Engine   │
                         └─────────────┬─────────────┘
                                       │
                                       ├──► Live Text Chunks over WebSocket (to UI)
                                       │
                                       └──► RabbitMQ Event: TranscriptionCompleted
```

### Core Responsibilities
1. **Unified WebSocket Endpoint (`/ws/transcribe`):** Accepts continuous binary media chunks routed from the React frontend via the Spring Cloud API Gateway (Port 8080)[cite: 1, 2].
2. **Audio Extraction & Normalization (FFmpeg):** 
   - **Video Input:** Runs an in-memory FFmpeg pipeline (`ffmpeg -i pipe:0 -f s16le -acodec pcm_s16le -ar 16000 -ac 1 pipe:1`) to demux the container, strip visual frames, and extract raw PCM audio[cite: 1].
   - **Audio Input:** Decodes and normalizes the incoming audio stream directly into 16 kHz mono PCM format[cite: 1].
3. **Speech-to-Text Execution (Faster-Whisper):** Processes the normalized audio buffer to generate low-latency text segments[cite: 1].
4. **Live Broadcast & Event Publishing:** Streams real-time transcript deltas back over the active WebSocket connection and publishes the `TranscriptionCompleted` event to RabbitMQ when recording stops[cite: 1, 3].

---

## 📂 Project Directory Structure

```text
E:\GitWork\notes-gen-ai\transcription-service\
├── venv/                    # Python Virtual Environment
├── app/
│   ├── __init__.py
│   ├── config.py            # Environment variables & service configurations
│   ├── audio_processor.py   # FFmpeg audio extraction & 16kHz PCM normalization
│   ├── transcriber.py       # Faster-Whisper model initialization & inference
│   └── messaging.py         # RabbitMQ publisher for TranscriptionCompleted events
├── main.py                  # FastAPI application entry point & WebSocket routes
├── requirements.txt         # Python package dependencies
├── Dockerfile               # Container definition for deployment
├── docker-compose.yml       # Local multi-container setup (Service + RabbitMQ)
├── .env                     # Local environment variables
└── README.md                # Service documentation
```

---

## 📄 Configuration Files

### 1. `requirements.txt`
Create `E:\GitWork\notes-gen-ai\transcription-service\requirements.txt`[cite: 1, 2, 3]:

```text
# Core FastAPI & ASGI Server
fastapi>=0.115.0
uvicorn[standard]>=0.30.0
pydantic>=2.9.0
websockets>=13.0

# Speech-to-Text & Audio Processing
faster-whisper>=1.0.3
ffmpeg-python>=0.2.0
numpy>=1.26.0

# Messaging (RabbitMQ)
aio-pika>=9.4.0

# Database / Storage Clients (Optional as required)
motor>=3.6.0
asyncpg>=0.30.0
boto3>=1.35.0

# Testing & Development
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.27.0

# Code Quality & Coverage
pytest-cov>=5.0.0
coverage[toml]>=7.6.0
ruff>=0.6.0
flake8>=7.1.0
black>=24.8.0
isort>=5.13.2
mypy>=1.11.0
bandit[toml]>=1.7.9
```

### 2. `requirements-dev.txt`
Create `E:\GitWork\notes-gen-ai\transcription-service\requirements-dev.txt`:

```text
# Development, Code Quality Check & Test Coverage Dependencies
-r requirements.txt

# Test Execution & Coverage
pytest>=8.0.0
pytest-asyncio>=0.23.0
pytest-cov>=5.0.0
coverage[toml]>=7.6.0
httpx>=0.27.0

# Code Quality - Linting & Formatting
ruff>=0.6.0
flake8>=7.1.0
black>=24.8.0
isort>=5.13.2

# Code Quality - Static Type Checking
mypy>=1.11.0

# Code Quality - Security Scanning
bandit[toml]>=1.7.9
```

### 3. `.env`
Create `E:\GitWork\notes-gen-ai\transcription-service\.env`[cite: 1, 3]:

```env
SERVICE_NAME=transcription-service
HOST=0.0.0.0
PORT=8082

# Faster-Whisper Configuration
WHISPER_MODEL_SIZE=base
WHISPER_DEVICE=cpu          # Set to 'cuda' for GPU or 'cpu' for local CPU
WHISPER_COMPUTE_TYPE=int8   # Set to 'float16' for GPU, 'int8' for CPU

# RabbitMQ Configuration (Port 5672)
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
TRANSCRIPTION_EXCHANGE=notes.events.exchange
TRANSCRIPTION_ROUTING_KEY=transcription.completed
```

---

## 🔌 API & WebSocket Endpoints

| Method / Protocol | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `http://localhost:8082/health` | Health check endpoint verifying service status[cite: 2]. |
| `GET` | `http://localhost:8082/docs` | Interactive Swagger UI API documentation. |
| `GET` | `http://localhost:8082/redoc` | ReDoc API documentation. |
| `WS` | `ws://localhost:8082/ws/transcribe` | Direct WebSocket endpoint for streaming audio/video chunks and receiving live transcripts[cite: 1, 2]. |
| `WS` | `ws://localhost:8080/ws/transcribe` | Proxied WebSocket endpoint via Spring Cloud API Gateway[cite: 1]. |