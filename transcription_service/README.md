# Transcription Service API

A production-grade FastAPI backend for audio transcription, featuring strict input validation, centralized structured logging, dynamic configuration management, code formatting, comprehensive test coverage, and mutation testing.

---

## 1. Project Overview & Features

- **Framework:** FastAPI with Uvicorn ASGI server.
- **Configuration Management:** Pydantic Settings (`pydantic-settings`) with dynamic metadata extraction and `.env` loading.
- **Structured Logging:** Centralized logging with environment-aware formatting:
  - Human-readable standard format in `development`.
  - Production-ready JSON logs via `python-json-logger` for non-development environments (`production`, `staging`, `ci`).
- **Code Quality & Formatting:** Fast linting, import sorting, and code formatting via `Ruff`.
- **Test Coverage:** Automated `pytest` suite with `pytest-cov` enforcing `>= 90%` statement coverage threshold.
- **Mutation Testing:** Robust test quality verification using `cosmic-ray` (cross-platform / native Windows) and `mutmut` (Linux / WSL / CI).

---

## 2. Project Structure

```text
transcription_service/
├── app/
│   ├── api/                  # API routes and endpoints
│   ├── core/
│   │   ├── config.py         # Application settings (Pydantic BaseSettings)
│   │   └── logger.py         # Centralized logging configuration
│   ├── services/             # Core business and transcription services
│   └── main.py               # FastAPI application factory & instance
├── tests/
│   ├── core/
│   │   ├── test_config.py    # Unit tests for settings and metadata
│   │   └── test_logger.py    # Unit tests for logging and formatters
│   └── test_api.py           # Integration tests for FastAPI endpoints
├── cosmic_ray.toml           # Cosmic-Ray mutation testing configuration
├── pyproject.toml            # Project dependencies, Ruff, Pytest, and Mutmut configs
└── README.md
```

---

## 3. Setup & Installation

### Prerequisites
- Python `>= 3.10`

### 1. Create and Activate Virtual Environment

* **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

* **Windows (PowerShell):**
  ```bash
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

* **Windows (Command Prompt):**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate.bat
  ```

### 2. Install Dependencies

Install the package in editable mode along with all development, testing, formatting, and mutation testing tools:

```bash
pip install -e ".[dev]"
```

---

## 4. Running the Application

### Start Development Server
```bash
uvicorn app.main:app --reload
```

### API Endpoints & Documentation
Once running, access the interactive documentation in your browser:
- **Interactive Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI Schema (JSON):** [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 5. Configuration & Environment Variables

Settings are managed via `app.core.config.Settings` and can be overridden via environment variables or a local `.env` file:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `ENVIRONMENT` | `development` | Deployment environment (`development`, `production`, `staging`, `ci`) |
| `LOG_LEVEL` | `INFO` | Global root logger level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) |
| `API_PREFIX` | `/api/v1` | URL routing prefix for all API endpoints |

Example `.env` file:
```dotenv
ENVIRONMENT=development
LOG_LEVEL=DEBUG
API_PREFIX=/api/v1
```

---

## 6. Code Quality & Formatting (`Ruff`)

The project uses [Ruff](https://github.com/astral-sh/ruff) for fast linting, import sorting (isort), and code formatting configured in `pyproject.toml`.

### Check Formatting (without modifying code)
```bash
ruff format --check .
```

### Auto-Format Codebase
```bash
ruff format .
```

### Run Linter
```bash
ruff check .
```

### Auto-Fix Fixable Lint Issues & Organize Imports
```bash
ruff check . --fix
```

---

## 7. Testing & Code Coverage

Tests are executed with `pytest` and tracked with `pytest-cov`. The test configuration in `pyproject.toml` automatically enforces a **90% minimum coverage threshold** and outputs a terminal summary plus an HTML report.

### Run All Tests with Coverage
```bash
pytest
```

### View HTML Coverage Report
After running pytest, open the generated HTML report:
* **Windows (PowerShell):**
  ```bash
  Start-Process htmlcov/index.html
  ```
* **macOS:**
  ```bash
  open htmlcov/index.html
  ```
* **Linux:**
  ```bash
  xdg-open htmlcov/index.html
  ```

### Run Specific Test Files
```bash
# Test API endpoints
pytest tests/test_api.py

# Test core configuration
pytest tests/core/test_config.py

# Test logger
pytest tests/core/test_logger.py
```

### Run Tests Quickly (without coverage overhead)
```bash
pytest -o addopts=""
```

---

## 8. Mutation Testing

Mutation testing introduces deliberate artificial faults (mutants) into your application code to verify whether your test suite actually catches logic changes and assertion gaps.

### Option A: `cosmic-ray` (Cross-Platform / Windows Compatible)

Configured via `cosmic_ray.toml`.

#### 1. Baseline Test Execution
Verify unmutated code passes all tests:
```bash
cosmic-ray baseline cosmic_ray.toml
```

#### 2. Initialize Mutation Session
Scan source code and prepare the mutation jobs database:
```bash
cosmic-ray init cosmic_ray.toml session.sqlite --force
```

#### 3. Apply Pragma Filters
Skip boilerplate entrypoint lines annotated with `# pragma: no mutate`:
```bash
cr-filter-pragma session.sqlite
```

#### 4. Execute Mutation Testing
Run tests against all generated mutants:
```bash
cosmic-ray exec cosmic_ray.toml session.sqlite
```

#### 5. View Mutation Reports

* **Terminal Summary Report:**
  ```bash
  cr-report session.sqlite
  ```

* **View Detailed Diffs and Test Outputs in Terminal:**
  ```bash
  cr-report --show-diff --show-output session.sqlite
  ```

* **Check Survival Rate:**
  ```bash
  cr-rate session.sqlite
  # 0.00 indicates 0% survived = 100% killed
  ```

* **Generate & Open Interactive HTML Report:**
  ```bash
  cr-html session.sqlite > mutation_report.html
  ```
  Open `mutation_report.html` in your web browser:
  ```bash
  Start-Process mutation_report.html    # Windows PowerShell
  open mutation_report.html             # macOS
  xdg-open mutation_report.html         # Linux
  ```

---

### Option B: `mutmut` (Linux / WSL / CI)

Configured via `[tool.mutmut]` in `pyproject.toml`.

> **Note for Windows:** `mutmut` relies on POSIX process forking. On Windows systems, run `mutmut` inside WSL (Windows Subsystem for Linux).

```bash
# Run mutation tests
mutmut run

# View mutation results summary
mutmut results

# View details/diff for a specific mutant ID
mutmut show <mutant_id>

# Open interactive terminal browser for mutation results
mutmut browse
```