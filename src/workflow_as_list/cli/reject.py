# src/workflow_as_list/cli/reject.py
"""workflow reject command - Reject workflows."""

import typer
from rich.console import Console

from ..config import load_config
from ..constants import ensure_directories
from ..executor import Executor
from ..models import AuditStatus, OutputType

console = Console()


def print_output(type: OutputType, message: str):
    """Print formatted output with [TYPE] prefix."""
    console.print(f"[{type.value}] {message}")


def reject(name: str = typer.Argument(..., help="Workflow name to reject")):
    """Reject a workflow."""
    ensure_directories()
    config = load_config()
    executor = Executor(config)

    workflow = executor.get_workflow(name)
    if not workflow:
        print_output(OutputType.ERROR, f"Workflow not found: {name}")
        raise typer.Exit(4)

    executor.update_workflow_status(name, AuditStatus.REJECTED)
    print_output(OutputType.SUCCESS, f"Workflow rejected: {name}")
