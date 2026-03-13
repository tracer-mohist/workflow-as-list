# src/workflow_as_list/server/__init__.py
"""Server module - FastAPI application and lifecycle management.

Exports:
- create_app: Create FastAPI application
- app: FastAPI application instance (for uvicorn)
- ServerManager: Server lifecycle management functions
"""

from .app import create_app
from .manager import (
    get_pid,
    is_running,
    logs,
    print_status,
    start,
    status,
    stop,
)

# For uvicorn: workflow_as_list.server:app
app = create_app()

__all__ = [
    "app",
    "create_app",
    "is_running",
    "get_pid",
    "start",
    "stop",
    "status",
    "logs",
    "print_status",
]
