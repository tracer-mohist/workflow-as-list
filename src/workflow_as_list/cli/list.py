"""workflow list command - List all registered workflows."""

from rich.console import Console

from ..constants import ensure_directories
from ..executor import Executor
from ..models import AuditStatus, OutputType

console = Console()


def print_output(type: OutputType, message: str):
    """Print formatted output with [TYPE] prefix."""
    console.print(f"[{type.value}] {message}")


def list_workflows():
    """List all registered workflows."""
    ensure_directories()
    executor = Executor()

    workflows = executor.list_workflows()

    if not workflows:
        print_output(OutputType.INFO, "No workflows registered")
        return

    print_output(OutputType.INFO, f"Registered workflows: {len(workflows)}")
    for wf in workflows:
        status_icon = "✓" if wf.status == AuditStatus.APPROVED else "○"
        console.print(f"  {status_icon} {wf.name} ({wf.status.value})")
