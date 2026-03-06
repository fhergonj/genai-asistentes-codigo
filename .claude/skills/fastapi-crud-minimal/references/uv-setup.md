# UV Project Setup

## Initialize Project with uv

```bash
# Create directory
mkdir my-api
cd my-api

# Initialize Python project with uv
uv init

# Create virtual environment and install dependencies
uv sync
```

## Add Dependencies

```bash
# Add main dependencies
uv add fastapi sqlmodel uvicorn

# Syntax: uv add <package> [<package2> ...]
```

## Generated Files

After `uv init`:
- `pyproject.toml` - Project configuration and dependencies
- `uv.lock` - Locked dependency versions (commit to version control)
- `.python-version` - Python version specification

## Common Commands

```bash
# Install/sync dependencies
uv sync

# Run Python
uv run python main.py

# Run with uvicorn
uv run uvicorn main:app --reload

# Add a package
uv add <package>

# Add dev dependency
uv add --dev pytest

# Remove package
uv remove <package>
```

## pyproject.toml Example

```toml
[project]
name = "my-api"
version = "0.1.0"
description = "FastAPI CRUD API"
requires-python = ">=3.11"
dependencies = [
    "fastapi==0.128.0",
    "sqlmodel>=0.0.18",
    "uvicorn[standard]>=0.24.0",
]

[tool.uv]
python-version = "3.11"
```

## Running the API

```bash
# With auto-reload (development)
uv run uvicorn main:app --reload

# Production
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

Access at: http://localhost:8000
Swagger docs: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
