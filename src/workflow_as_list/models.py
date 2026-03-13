# src/workflow_as_list/models.py
"""Data models for workflow management."""

from datetime import UTC, datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


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
    Stored in ~/.config/wf/executions/<name>-<timestamp>.json
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


class Config(BaseModel):
    """Application configuration.

    Loaded from INI files with this priority:
    1. Built-in defaults
    2. ~/.config/workflow/config.ini (user)
    3. ./workflow.ini (project)
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
        default_factory=lambda: str(Path.home() / ".workflow-as-list")
    )

    # Token length constraints (from design docs)
    token_min: int = Field(default=282)
    token_max: int = Field(default=358)
