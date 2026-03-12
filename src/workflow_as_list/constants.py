# src/workflow_as_list/constants.py
"""Centralized constants and path definitions.

Single source of truth for all paths and configuration constants.
"""

from pathlib import Path

# =============================================================================
# Base Directory
# =============================================================================

BASE_DIR = Path.home() / ".workflow-as-list"

# =============================================================================
# Configuration Files
# =============================================================================

CONFIG_FILE = BASE_DIR / "config.ini"
REGISTRY_FILE = BASE_DIR / "registry.jsonl"

# =============================================================================
# Server Files
# =============================================================================

PID_FILE = BASE_DIR / "server.pid"
SERVER_LOG = BASE_DIR / "server.log"

# =============================================================================
# State Directories
# =============================================================================

STATE_DIR = BASE_DIR / "state"
EXECUTIONS_DIR = STATE_DIR / "executions"
OUTPUTS_DIR = STATE_DIR / "outputs"

# =============================================================================
# Cache Directories
# =============================================================================

CACHE_DIR = BASE_DIR / "cache"
IMPORTS_CACHE = CACHE_DIR / "imports"

# =============================================================================
# Server Defaults
# =============================================================================

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080

# =============================================================================
# Token Constraints
# =============================================================================

TOKEN_MIN = 282
TOKEN_MAX = 358


# =============================================================================
# Directory Initialization
# =============================================================================


def ensure_directories() -> None:
    """Ensure all required directories exist.

    Creates BASE_DIR and all subdirectories on first use.
    """
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    EXECUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    IMPORTS_CACHE.mkdir(parents=True, exist_ok=True)
