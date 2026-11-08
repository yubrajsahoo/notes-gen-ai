# Transcription Service

A high-performance asynchronous Transcription API service built with [FastAPI](https://fastapi.tiangolo.com/), [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/), and [Uvicorn](https://www.uvicorn.org/), managed using [uv](https://docs.astral.sh/uv/).

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Getting Started](#getting-started)
  - [1. Clone Repository](#1-clone-repository)
  - [2. Environment Configuration](#2-environment-configuration)
  - [3. Install Dependencies](#3-install-dependencies)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Code Quality & Linting](#code-quality--linting)
  - [Ruff Check (Linting)](#ruff-check-linting)
  - [Ruff Format (Formatting)](#ruff-format-formatting)
- [Running Tests](#running-tests)
- [Configuration Reference](#configuration-reference)

---

## Features

- **FastAPI Framework**: High performance, type-annotated asynchronous web endpoints.
- **Pydantic Settings Management**: Environment-based configuration with automatic `.env` loading and case-insensitive attribute access.
- **Structured Logging**: Unified console logging with custom formatting and integration with Uvicorn loggers.
- **CORS Middleware**: Flexible Cross-Origin Resource Sharing (CORS) configurable via environment variables.
- **Development Tooling**: Fast dependency management with `uv`, code formatting & linting with `ruff`, and testing with `pytest` & `pytest-cov`.

---

## Project Structure

```text
transcription-service/
├── .env.example                               # Sample environment variables
├── pyproject.toml                             # Project metadata, dependencies & tool configs
├── README.md                                  # Project documentation
├── src/
│   └── transcription_service/
│       ├── __init__.py                        # Package root
│       ├── main.py                            # FastAPI application entrypoint & server runner
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py                      # Pydantic Settings and environment config
│       │   ├── logger.py                      # Centralized logging configuration
│       │   └── middle_ware.py                 # CORS & application middleware setup
│       └── routes/
│           ├── __init__.py
│           ├── router.py                      # Main API router registry
│           ├── common/
│           │   ├── __init__.py
│           │   └── health.py                  # Health check endpoints
│           └── v1/
│               └── __init__.py                # API v1 routes
└── tests/
    ├── transcription_service/
    │   ├── test_main.py                       # Tests for FastAPI app, middleware & CLI
    │   ├── test_init.py                       # Tests for root module entrypoint
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── test_config.py                 # Tests for settings & environment variables
    │   │   ├── test_logger.py                 # Tests for logging setup
    │   │   └── test_middle_ware.py            # Tests for CORS middleware
    │   └── routes/
    │       ├── test_router.py                 # Tests for main API router registry
    │       └── common/
    │           ├── __init__.py
    │           └── test_health.py             # Tests for health endpoints
    └── resources/
```

---

## Requirements

- **Python**: `>= 3.14`
- **uv**: `>= 0.5.0` (Fast Python package and environment manager)

---

## Getting Started

### 1. Clone Repository

```bash
git clone <repository-url>
cd transcription-service
```

### 2. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Adjust variables in `.env` as needed.

### 3. Install Dependencies

Install all dependencies including development tools (`pytest`, `ruff`, `pytest-cov`) using `uv`:

```bash
uv sync
```

---

## Running the Application

### Option 1: Direct Module Execution (Recommended for Dev)

```bash
uv run python -m transcription_service.main
```

### Option 2: Using Uvicorn CLI

```bash
uv run uvicorn transcription_service.main:app --host 127.0.0.1 --port 8000 --reload
```

### Option 3: Using the Project Script Entrypoint

```bash
uv run transcription-service
```

Once started, the application will be accessible at:
- **API Root**: `http://localhost:8000/`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## API Endpoints

| Method | Path | Description | Response |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Service health check | `{"status": "healthy"}` |
| `GET` | `/health` | Service health check alias | `{"status": "healthy"}` |
| `GET` | `/docs` | Interactive Swagger UI documentation | HTML |
| `GET` | `/redoc` | ReDoc API documentation | HTML |

---

## Code Quality & Linting

This project uses [Ruff](https://docs.astral.sh/ruff/) for fast Python linting and code formatting.

### Ruff Check (Linting)

Check for linting errors across the codebase:

```bash
uv run ruff check
```

Automatically fix supported linting errors:

```bash
uv run ruff check --fix
```

Check a specific path or file:

```bash
uv run ruff check src/
uv run ruff check tests/
```

### Ruff Format (Formatting)

Verify that files are correctly formatted without modifying them:

```bash
uv run ruff format --check
```

Format all files in the project according to style rules:

```bash
uv run ruff format
```

Format a specific file or folder:

```bash
uv run ruff format src/
uv run ruff format tests/
```

---

## Running Tests

Tests are written using `pytest` and `pytest-cov`.

### Run All Tests

```bash
uv run pytest
```

### Run Tests with Coverage Report

```bash
uv run pytest --cov=transcription_service --cov-report=term-missing
```

### Run Specific Test Modules

```bash
# Main application tests
uv run pytest tests/transcription_service/test_main.py

# Route tests
uv run pytest tests/transcription_service/routes/test_router.py
uv run pytest tests/transcription_service/routes/common/test_health.py

# Core tests
uv run pytest tests/transcription_service/core/test_config.py
uv run pytest tests/transcription_service/core/test_logger.py
uv run pytest tests/transcription_service/core/test_middle_ware.py
```

---

## Configuration Reference

The application uses Pydantic Settings configured in `src/transcription_service/core/config.py`. Values can be set via `.env` file or environment variables:

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `PROJECT_NAME` | `str` | `"Transcription API"` | Application title shown in OpenAPI documentation |
| `HOST` | `str` | `"localhost"` | Host address for the HTTP server |
| `PORT` | `int` | `8000` | Port for the HTTP server |
| `RELOAD` | `bool` | `True` | Enable auto-reload on code changes (development) |
| `DEBUG` | `bool` | `True` | Enable debug mode and verbose logging (`DEBUG` level) |
| `CORS_ORIGINS` | `list[str]` | `["*"]` | Allowed CORS origins (JSON list or comma-separated) |
