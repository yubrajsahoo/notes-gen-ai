@echo off
setlocal

:: =============================================================================
:: Build & Quality Verification Script for Transcription Service
:: =============================================================================
:: Performs complete build verification:
::   1. Environment & Virtualenv Validation
::   2. Python Syntax & Bytecode Compilation Check
::   3. Code Quality Linting (Ruff)
::   4. PEP 8 Compliance Check (Flake8)
::   5. Code Formatting Check (Black)
::   6. Import Order Verification (isort)
::   7. Static Type Checking (Mypy)
::   8. Security Vulnerability Scanning (Bandit)
::   9. Unit Tests & Code Coverage Enforcement (Pytest + Coverage)
::  10. Application Smoke / Startup Verification (FastAPI App Import)
:: =============================================================================

cd /d "%~dp0"
title Transcription Service - Build and Quality Checks

echo ===============================================================================
echo                TRANSCRIPTION SERVICE - BUILD ^& QUALITY CHECKS
echo ===============================================================================
echo Project Directory: %CD%
echo.

:: -----------------------------------------------------------------------------
:: 1. Virtual Environment Detection
:: -----------------------------------------------------------------------------
set "PYTHON_EXE=venv\Scripts\python.exe"
set "PIP_EXE=venv\Scripts\pip.exe"
set "PYTEST_EXE=venv\Scripts\pytest.exe"
set "RUFF_EXE=venv\Scripts\ruff.exe"
set "FLAKE8_EXE=venv\Scripts\flake8.exe"
set "BLACK_EXE=venv\Scripts\black.exe"
set "ISORT_EXE=venv\Scripts\isort.exe"
set "MYPY_EXE=venv\Scripts\mypy.exe"
set "BANDIT_EXE=venv\Scripts\bandit.exe"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Virtual environment not found at 'venv\'.
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [FATAL] Failed to create virtual environment with system Python.
        exit /b 1
    )
    echo Installing dependencies from requirements-dev.txt...
    "%PIP_EXE%" install --upgrade pip
    "%PIP_EXE%" install -r requirements-dev.txt
    if errorlevel 1 (
        echo [FATAL] Failed to install development dependencies.
        exit /b 1
    )
)

echo [INFO] Using Python:
"%PYTHON_EXE%" --version
echo.

:: Parameter Handling: allow --install or -i to re-sync dependencies
if "%1"=="--install" goto :INSTALL_DEPS
if "%1"=="-i" goto :INSTALL_DEPS
goto :START_CHECKS

:INSTALL_DEPS
echo [STEP 0/10] Installing / Updating Dependencies from requirements-dev.txt...
"%PIP_EXE%" install -r requirements-dev.txt
if errorlevel 1 (
    echo [ERROR] Dependency installation failed.
    exit /b 1
)
echo [OK] Dependencies up to date.
echo.

:START_CHECKS
:: -----------------------------------------------------------------------------
:: Step 1: Bytecode & Syntax Compilation
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [STEP 1/10] Syntax ^& Bytecode Compilation Check...
echo ===============================================================================
"%PYTHON_EXE%" -m compileall app test -q
if errorlevel 1 (
    echo [FAIL] Syntax errors detected in app or test packages.
    exit /b 1
)
"%PYTHON_EXE%" -m py_compile main.py
if errorlevel 1 (
    echo [FAIL] Syntax error detected in main.py.
    exit /b 1
)
echo [PASS] All source files compiled successfully.
echo.

:: -----------------------------------------------------------------------------
:: Step 2: Ruff Linter
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [STEP 2/10] Ruff Code Quality Check...
echo ===============================================================================
"%RUFF_EXE%" check .
if errorlevel 1 (
    echo [FAIL] Ruff linting checks failed.
    exit /b 1
)
echo [PASS] Ruff checks passed.
echo.

:: -----------------------------------------------------------------------------
:: Step 3: Flake8 Linter
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [STEP 3/10] Flake8 PEP 8 Compliance Check...
echo ===============================================================================
"%FLAKE8_EXE%" --config=.flake8
if errorlevel 1 (
    echo [FAIL] Flake8 compliance check failed.
    exit /b 1
)
echo [PASS] Flake8 checks passed.
echo.

:: -----------------------------------------------------------------------------
:: Step 4: Black Formatting Check
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [STEP 4/10] Black Formatting Verification...
echo ===============================================================================
"%BLACK_EXE%" --check .
if errorlevel 1 (
    echo [FAIL] Black formatting check failed. Run 'black .' to auto-format.
    exit /b 1
)
echo [PASS] Black formatting verified.
echo.

:: -----------------------------------------------------------------------------
:: Step 5: isort Import Sorting Check
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [STEP 5/10] isort Import Ordering Verification...
echo ===============================================================================
"%ISORT_EXE%" --check-only .
if errorlevel 1 (
    echo [FAIL] Import sorting check failed. Run 'isort .' to auto-sort imports.
    exit /b 1
)
echo [PASS] Import sorting verified.
echo.

:: -----------------------------------------------------------------------------
:: Step 6: Mypy Static Type Checking
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [STEP 6/10] Mypy Static Type Analysis...
echo ===============================================================================
"%MYPY_EXE%" app
if errorlevel 1 (
    echo [FAIL] Mypy static type checking failed.
    exit /b 1
)
echo [PASS] Mypy type checks passed.
echo.

:: -----------------------------------------------------------------------------
:: Step 7: Bandit Security Scanner
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [STEP 7/10] Bandit Security Vulnerability Scan...
echo ===============================================================================
"%BANDIT_EXE%" -c pyproject.toml -r app
if errorlevel 1 (
    echo [FAIL] Bandit identified security vulnerabilities.
    exit /b 1
)
echo [PASS] Bandit security scan passed.
echo.

:: -----------------------------------------------------------------------------
:: Step 8: Pytest Unit Tests & Code Coverage
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [STEP 8/10] Pytest Suite ^& Test Coverage Enforcement...
echo ===============================================================================
"%PYTEST_EXE%"
if errorlevel 1 (
    echo [FAIL] Unit tests or minimum coverage threshold failed.
    exit /b 1
)
echo [PASS] All unit tests passed with required coverage.
echo.

:: -----------------------------------------------------------------------------
:: Step 9: FastAPI Application Smoke Test
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [STEP 9/10] FastAPI Application Smoke / Import Test...
echo ===============================================================================
"%PYTHON_EXE%" -c "from main import app; assert app.title == 'Notes-Gen-AI Transcription Service'; print('[SMOKE TEST] FastAPI app initialized successfully.')"
if errorlevel 1 (
    echo [FAIL] Application smoke test failed.
    exit /b 1
)
echo [PASS] FastAPI application startup verified.
echo.

:: -----------------------------------------------------------------------------
:: Step 10: Docker Build Check (Optional if Docker is present)
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo [STEP 10/10] Docker Verification (Optional)...
echo ===============================================================================
if exist "Dockerfile" (
    docker info >nul 2>&1
    if not errorlevel 1 (
        echo [INFO] Building Docker container 'notes-gen-ai/transcription-service:test'...
        docker build -t notes-gen-ai/transcription-service:test .
        if errorlevel 1 (
            echo [FAIL] Docker build failed.
            exit /b 1
        )
        echo [PASS] Docker image built successfully.
    ) else (
        echo [SKIP] Docker daemon is not running. Skipping container build.
    )
) else (
    echo [SKIP] No Dockerfile found in root directory. Skipping container build.
)
echo.

:: -----------------------------------------------------------------------------
:: Build Success Summary
:: -----------------------------------------------------------------------------
echo ===============================================================================
echo                         BUILD SUCCESSFUL
echo ===============================================================================
echo All 10 build, quality, security, and coverage checks passed successfully.
echo HTML coverage report generated at: coverage_html\index.html
echo ===============================================================================
exit /b 0
