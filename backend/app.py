"""
LEGACY Flask entry point — deprecated.

Use FastAPI instead:
    uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

This file is kept for reference only and will not start without
Flask blueprint exports that were removed during the FastAPI migration.
"""

import sys

print(
    "WARNING: backend/app.py (Flask) is deprecated.\n"
    "Start the API with: uvicorn backend.main:app --host 127.0.0.1 --port 8000",
    file=sys.stderr,
)
sys.exit(1)
