# Python 3.12 Migration Requirement

## 1. Problem Statement

The `ioit.acm` project is currently configured for Python 2.7, which reached end-of-life in 2020. The migration to Python 3.12 is required to ensure the project remains secure, maintainable, and compatible with modern library ecosystems. The Python 2.7 references are embedded across version configuration, Docker base image, Makefile venv creation, and Python 2-specific syntax in the source code.

## 2. Current State

### Current Python version references
- `.python-version`: `2.7.18`
- `Dockerfile`: `FROM python:2.7`
- `Makefile`: `python2 -m venv venv`

### Current dependency management
- `requirements.txt` with 9 packages: Flask, Gunicorn, requests, python-dotenv, Flask-SQLAlchemy, flask-login, pymysql, flask_limiter, Flask-Mail
- No `pyproject.toml` or `setup.py` — uses legacy `requirements.txt` format

### Current Docker Python environment
- Base image: `python:2.7`
- Installs `requirements.txt` via pip
- Runs `python run.py` as entry point

### Current CI/CD Python environment
- `.github/workflows/deploy.yml` runs on `ubuntu-latest`
- No explicit Python version specified in the workflow
- Depends on remote server deployment script (`deploy.sh`)

### Relevant Python configuration
- No `pyproject.toml`, `setup.py`, or `tox.ini`
- Version controlled solely by `.python-version` file and Dockerfile

### Python 2 remnants discovered
- `app/blueprints/events.py:30`: `urllib.quote(name.encode("utf-8"))` — Python 2 function removed in Python 3
- `app/blueprints/events.py:34`: `urllib.unquote(slug).decode("utf-8")` — Python 2 function removed in Python 3

## 3. Migration Requirements

### Mandatory changes
1. **`.python-version`**: Change from `2.7.18` to `3.12`
2. **`Dockerfile`**: Change base image from `python:2.7` to `python:3.12`
3. **`Makefile`**: Change `python2` to `python3` for venv creation
4. **`app/blueprints/events.py`**: Replace `urllib.quote()` with `urllib.parse.quote()` and `urllib.unquote()` with `urllib.parse.unquote()`

### Compatibility fixes
5. Verify all 9 packages in `requirements.txt` are compatible with Python 3.12 (Flask >= 2.3, Gunicorn >= 21.2, requests >= 2.28, python-dotenv >= 1.0.0, Flask-SQLAlchemy >= 3.1, flask-login >= 0.5, pymysql >= 1.0, flask_limiter >= 3.2, Flask-Mail >= 0.8) — already installed and working on Python 3.14, confirming compatibility
6. Ensure no other Python 2-specific syntax exists in the codebase (confirmed: only the `urllib.quote`/`urllib.unquote` calls found)

### Dependency changes
7. No dependency upgrades required — all 9 packages in `requirements.txt` support Python 3.12 with their current versions
8. No new dependencies needed

### Docker/environment changes
9. Update Dockerfile to use `python:3.12` base image
10. Ensure `pip install -r requirements.txt` works with Python 3.12 (confirmed working on Python 3.14)

### CI/CD changes
11. Optionally add Python version specification to `.github/workflows/deploy.yml` for consistency (e.g., `setup-python` action), but this is optional since the workflow delegates to a remote deployment script

### Validation/testing requirements
12. Application should import and run without errors under Python 3.12
13. The `urllib.parse` migration should be verified (`urllib.quote`/`urllib.unquote` → `urllib.parse.quote`/`urllib.parse.unquote`)
14. Docker build should succeed with `python:3.12` base image
15. `make run` (or `flask run`) should start the application successfully

## 4. Non-Requirements

- Do not upgrade unrelated packages merely because newer versions exist
- Do not refactor application code without a Python 3.12 compatibility reason
- Do not change the application's feature set or architecture
- Do not modify Node.js/Tailwind configuration unrelated to Python runtime
- Do not modify `.env.example` or environment variable definitions
- Do not change the deployment target or remote server configuration

## 5. Acceptance Criteria

The migration will be complete when all of the following conditions are met:

1. `.python-version` contains `3.12` (or `3.12.x`)
2. `Dockerfile` uses `python:3.12` as the base image
3. `Makefile` uses `python3` for venv creation
4. `app/blueprints/events.py` uses `urllib.parse.quote()` and `urllib.parse.unquote()` (no `urllib.quote` or `urllib.unquote`)
5. The application can be imported and started under Python 3.12 without errors
6. Docker builds successfully with `python:3.12`
7. All existing functionality (routes, API endpoints, database operations) continues to work
