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

"""
All workflow-as-list state lives here.

Why:
- Single location (easy to remember for agents)
- Easy cleanup: rm -rf ~/.workflow-as-list/
- Easy backup: backup one directory
- State visible: always know where to look
"""
PROJECT_ROOT = Path.home() / ".workflow-as-list"
LOGS_ROOT = PROJECT_ROOT / "logs"

# =============================================================================
# Configuration Files
# =============================================================================

CONFIG_FILE = PROJECT_ROOT / "config.ini"
REGISTRY_FILE = PROJECT_ROOT / "registry.jsonl"

# =============================================================================
# Server Files
# =============================================================================

PID_FILE = PROJECT_ROOT / "server.pid"
SERVER_LOG = LOGS_ROOT / "server.log"

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
# Token Constraints (Hub Token Bounds)
# =============================================================================

TOKEN_HUB_LOWER = 282
"""
Recommended minimum hub tokens for complete task description.

Why: Task descriptions below this may lack context for reliable execution.
Strategy: If below, warn user to consider adding constraints or preconditions.
Reference: docs/research/theory/003-limits.md (Effective Context Square Root Formula)
"""

TOKEN_HUB_UPPER = 358
"""
Maximum hub tokens before task decomposition required.

Why: Complex descriptions increase execution ambiguity.
Strategy: Apply Divide and Conquer - decompose into parent + subtasks.
Reference: docs/research/theory/003-limits.md (Effective Context Square Root Formula)
"""

# =============================================================================
# Directory Initialization
# =============================================================================


def ensure_directories() -> None:
    """Ensure all required directories exist.

    Creates PROJECT_ROOT and all subdirectories on first use.
    """
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    LOGS_ROOT.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    EXECUTIONS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    IMPORTS_CACHE.mkdir(parents=True, exist_ok=True)
