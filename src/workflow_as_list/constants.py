# src/workflow_as_list/constants.py
"""Centralized constants and path definitions.

Single source of truth for all paths and configuration constants.

Design Principle: All state lives under PROJECT_ROOT for easy cleanup,
backup, and agent-friendly state visibility.
"""

from pathlib import Path

# =============================================================================
# Project Root
# =============================================================================

PROJECT_ROOT = Path.home() / ".workflow-as-list"
"""
All workflow-as-list state lives here.

Why:
- Single location (easy to remember for agents)
- Easy cleanup: rm -rf ~/.workflow-as-list/
- Easy backup: backup one directory
- State visible: always know where to look
"""

# =============================================================================
# Configuration Files
# =============================================================================

CONFIG_FILE = PROJECT_ROOT / "config.ini"
REGISTRY_FILE = PROJECT_ROOT / "registry.jsonl"

# =============================================================================
# Server Files
# =============================================================================

PID_FILE = PROJECT_ROOT / "server.pid"
SERVER_LOG = PROJECT_ROOT / "logs" / "server.log"

# =============================================================================
# State Directories
# =============================================================================

STATE_DIR = PROJECT_ROOT / "state"
EXECUTIONS_DIR = STATE_DIR / "executions"
OUTPUTS_DIR = STATE_DIR / "outputs"

# =============================================================================
# Cache Directories
# =============================================================================

CACHE_DIR = PROJECT_ROOT / "cache"
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

    Creates PROJECT_ROOT and all subdirectories on first use.
    """
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    EXECUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    IMPORTS_CACHE.mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / "logs").mkdir(parents=True, exist_ok=True)
