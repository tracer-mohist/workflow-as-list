# src/workflow_as_list/cli/check.py
"""workflow check command - Validate and register workflow files."""

from pathlib import Path

import typer
from rich.console import Console

from ..config import load_config
from ..constants import ensure_directories
from ..executor import Executor, WorkflowParser
from ..models import OutputType
from ..security import compute_hash, run_security_checks

console = Console()


def print_output(type: OutputType, message: str):
    """Print formatted output with [TYPE] prefix."""
    console.print(f"[{type.value}] {message}")


def check(
    file: Path = typer.Argument(..., help="Workflow file to validate and register"),
):
    """Validate and register a workflow file."""
    ensure_directories()
    cfg = load_config()
    executor = Executor(Path(cfg.config_dir))

    # Read file
    if not file.exists():
        print_output(OutputType.ERROR, f"File not found: {file}")
        raise typer.Exit(1)

    content = file.read_text()
    file_hash = compute_hash(file)

    # Run security checks (skip Layer 5 - audit status check)
    passed, errors = run_security_checks(
        content, cfg, "pending_audit", skip_audit_check=True
    )

    if not passed:
        print_output(OutputType.ERROR, "Security checks failed:")
        for error in errors:
            console.print(f"  - {error}")
        raise typer.Exit(3)

    # Parse workflow
    parser = WorkflowParser(content)
    steps = parser.parse()

    # Register
    workflow = executor.register_workflow(
        name=file.stem,
        file_path=file,
        content=content,
        file_hash=file_hash,
        token_count=len(content.encode("utf-8")),
    )

    print_output(OutputType.SUCCESS, f"Workflow registered: {workflow.name}")
    print_output(OutputType.INFO, f"Steps: {len(steps)}")
    print_output(OutputType.NEXT, f"Run: workflow approve {workflow.name}")
