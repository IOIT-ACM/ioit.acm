# Python 3.12 Migration Requirement

## 1. Problem Statement

The `ioit.acm` project is currently configured for Python 2.7, which reached end-of-life in 2020. The migration to Python 3.12 is required to ensure the project remains secure, maintainable, and compatible with modern library ecosystems. The Python 2.7 references are embedded across version configuration, Docker base image, Makefile venv creation, and Python 2-specific syntax in the source code.

## 2. Current State

### Current Python version references
- `.python-version`: `3.12` (migrated)
- `Dockerfile`: `FROM python:3.12` (migrated)
- `Makefile`: `python3 -m venv venv` (migrated from `python2`)

### Current dependency management
- `pyproject.toml` with 9 packages and `uv.lock` for lockfile reproducibility
- No `requirements.txt` (replaced by `pyproject.toml` + `uv.lock`)

### Current Docker Python environment
- Base image: `python:3.12`
- Installs dependencies via `uv sync --frozen`

### Current CI/CD Python environment
- GitHub Actions workflows use `ubuntu-latest`
- No explicit Python version specified yet (can be added)

### Relevant Python configuration
- `.python-version`: `3.12`
- `dockerfile`: `python:3.12`

### Python 2 remnants discovered
- `app/blueprints/events.py:30`: `urllib.quote(name.encode("utf-8"))` → migrated to `urllib.parse.quote(name.encode("utf-8"))`
- `app/blueprints/events.py:34`: `urllib.unquote(slug).decode("utf-8")` → migrated to `urllib.parse.unquote(slug)` (removed `.decode("utf-8")` since Python 3's `unquote` returns `str`)

## 3. Migration Requirements

### Mandatory changes
1. **`.python-version`**: Change from `2.7.18` to `3.12`
2. **`Dockerfile`**: Change base image from `python:2.7` to `python:3.12`
3. **`Makefile`**: Change `python2` to `python3` for venv creation
4. **`app/blueprints/events.py`**: Replace `urllib.quote()` with `urllib.parse.quote()` and `urllib.unquote()` with `urllib.parse.unquote()`
5. **`pyproject.toml`**: Create with `requires-python = ">=3.12"` and 9 pinned dependencies
6. **`uv.lock`**: Generate with `uv lock` for reproducible installs
7. **`requirements.txt`**: Remove (replaced by `pyproject.toml` + `uv.lock`)
8. **`app/__init__.py`**: Fix `db.create_all()` for SQLAlchemy 2.x compatibility (use loop over `SQLALCHEMY_BINDS` keys)

### Compatibility fixes
9. Verify all 9 packages in `pyproject.toml` are compatible with Python 3.12 (Flask >= 2.3, Gunicorn >= 21.2, requests >= 2.28, python-dotenv >= 1.0.0, Flask-SQLAlchemy >= 3.1, flask-login >= 0.5, pymysql >= 1.0, flask_limiter >= 3.2, Flask-Mail >= 0.8) — verified via `uv sync`
10. Ensure no other Python 2-specific syntax exists in the codebase (confirmed: only the `urllib.quote`/`unquote` calls found and migrated)

### Dependency changes
11. No dependency upgrades required — all 9 packages support Python 3.12 with their current versions
12. No new dependencies needed

### Docker/environment changes
13. Update Dockerfile to use `python:3.12` base image and `uv sync --frozen`
14. Ensure `pip install -r requirements.txt` works with Python 3.12 (no longer needed after migration)

### CI/CD changes
15. Optionally add Python version specification to GitHub Actions workflows for consistency

### Validation/testing requirements
16. Application should import and run without errors under Python 3.12
17. The `urllib.parse` migration should be verified (`urllib.quote`/`urllib.unquote` → `urllib.parse.quote`/`urllib.parse.unquote`)
18. Docker build should succeed with `python:3.12` base image
19. `make install` (or `uv sync`) should install dependencies successfully

## 4. Non-Requirements

- Do not upgrade unrelated packages merely because newer versions exist
- Do not refactor application code without a Python 3.12 compatibility reason
- Do not change the application's feature set or architecture
- Do not modify Node.js/Tailwind configuration unrelated to Python runtime
- Do not modify `.env` or environment variable definitions
- Do not change the deployment target or remote server configuration

## 5. Acceptance Criteria

The migration will be complete when all of the following conditions are met:

1. `.python-version` contains `3.12` (or `3.12.x`)
2. `Dockerfile` uses `python:3.12` as the base image
3. `Makefile` uses `python3` for venv creation
4. `app/blueprints/events.py` uses `urllib.parse.quote()` and `urllib.parse.unquote()` (no `urllib.quote` or `urllib.unquote`)
5. The application can be imported and run under Python 3.12 without errors
6. Docker builds successfully with `python:3.12`
7. All existing functionality (routes, API endpoints, database operations) continues to work

## 6. Files Changed

| File | Change |
|------|--------|
| `.python-version` | `2.7.18` → `3.12` |
| `Dockerfile` | `python:2.7` → `python:3.12` |
| `Makefile` | `python2` → `python3` venv |
| `app/blueprints/events.py` | `urllib.quote/unquote` → `urllib.parse.quote/unquote` |
| `app/__init__.py` | Fixed `db.create_all()` for SQLAlchemy 2.x |
| `pyproject.toml` | Created with 9 pinned dependencies |
| `uv.lock` | Generated with 28 resolved packages |
| `requirements.txt` | Removed |
| `requirement.md` | Created with migration requirements |