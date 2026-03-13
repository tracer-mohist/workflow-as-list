# src/workflow_as_list/models.py
"""Data models for workflow management."""

from datetime import UTC, datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field

# Import token constants for Config defaults
from .constants import TOKEN_HUB_LOWER, TOKEN_HUB_UPPER


# Audit status for workflow lifecycle
class AuditStatus(str, Enum):
    """Workflow audit status."""

    PENDING_AUDIT = "pending_audit"
    APPROVED = "approved"
    REJECTED = "rejected"


# Execution status for runtime tracking
class ExecutionStatus(str, Enum):
    """Execution instance status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# Output types for CLI and server responses
# Used for [TYPE] prefix in agent-readable output
class OutputType(str, Enum):
    """Output message types."""

    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"
    NEXT = "NEXT"


class Workflow(BaseModel):
    """Workflow registry entry.

    Stored in registry.jsonl (append-only).
    """

    name: str = Field(..., description="Workflow name (filename without extension)")
    hash: str = Field(..., description="SHA256 hash of workflow file content")
    status: AuditStatus = Field(default=AuditStatus.PENDING_AUDIT)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    file_path: str = Field(..., description="Absolute path to workflow file")

    # Metadata for debugging and audit trail
    line_count: int = Field(default=0, description="Total lines in workflow")
    token_count: int = Field(default=0, description="Total bytes for token check")


class Execution(BaseModel):
    """Execution instance.

    Created when workflow.run() is called.
    Stored in PROJECT_ROOT/state/executions/<name>-<timestamp>.json

    Progressive reading design:
    - Agent must read current step before advancing (steps_read tracking)
    - steps_read contains indices of steps that have been read
    - next command checks if current_step is in steps_read
    """

    execution_id: str = Field(..., description="Unique execution identifier")
    workflow_name: str = Field(..., description="Reference to workflow")
    workflow_hash: str = Field(
        ..., description="Hash at execution start (immutability check)"
    )
    status: ExecutionStatus = Field(default=ExecutionStatus.PENDING)
    current_step: int = Field(default=0, description="Current step index (0-based)")
    started_at: datetime | None = None
    completed_at: datetime | None = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Execution state
    steps_total: int = Field(default=0, description="Total steps in workflow")
    outputs_path: str = Field(default="", description="Path to outputs directory")
    steps_read: list[int] = Field(
        default_factory=list,
        description="Indices of steps that have been read (progressive reading)",
    )


class Config(BaseModel):
    """Application configuration.

    Loaded from INI files with this priority:
    1. Built-in defaults (PROJECT_ROOT)
    2. PROJECT_ROOT/config.ini (unified config)
    3. ./workflow.ini (project override)
    4. CLI arguments (override)
    """

    # Security
    blacklist: list[str] = Field(default_factory=list)
    whitelist: list[str] = Field(default_factory=list)
    enable_whitelist: bool = Field(default=False, description="Opt-in whitelist check")

    # Server
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8080)

    # Paths
    config_dir: str = Field(
        default_factory=lambda: str(Path.home() / ".workflow-as-list"),
        description="Root directory for all workflow state",
    )

    # Token length constraints (from design docs)
    token_hub_lower: int = Field(
        default=TOKEN_HUB_LOWER,
        description="Recommended minimum hub tokens (warning if below)",
    )
    token_hub_upper: int = Field(
        default=TOKEN_HUB_UPPER,
        description="Maximum hub tokens before decomposition required (error if above)",
    )
