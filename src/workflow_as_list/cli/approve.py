"""workflow approve command - Approve workflows for execution."""

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


def approve(name: str = typer.Argument(..., help="Workflow name to approve")):
    """Approve a workflow for execution."""
    ensure_directories()
    config = load_config()
    executor = Executor(config)

    workflow = executor.get_workflow(name)
    if not workflow:
        print_output(OutputType.ERROR, f"Workflow not found: {name}")
        raise typer.Exit(4)

    if workflow.status == AuditStatus.APPROVED:
        print_output(OutputType.WARN, f"Workflow already approved: {name}")
        return

    executor.update_workflow_status(name, AuditStatus.APPROVED)
    print_output(OutputType.SUCCESS, f"Workflow approved: {name}")
    print_output(OutputType.NEXT, f"Run: workflow run {workflow.name}")
