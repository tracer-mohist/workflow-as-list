"""workflow show command - Show workflow or execution details."""

import typer
from rich.console import Console

from ..constants import ensure_directories
from ..executor import Executor
from ..models import OutputType

console = Console()


def print_output(type: OutputType, message: str):
    """Print formatted output with [TYPE] prefix."""
    console.print(f"[{type.value}] {message}")


def show(target: str = typer.Argument(..., help="Workflow name or execution ID")):
    """Show workflow or execution details."""
    ensure_directories()
    executor = Executor()

    # Try workflow first
    workflow = executor.get_workflow(target)
    if workflow:
        console.print(f"Workflow: {workflow.name}")
        console.print(f"  Status: {workflow.status.value}")
        console.print(f"  File: {workflow.file_path}")
        console.print(f"  Lines: {workflow.line_count}")
        console.print(f"  Tokens: {workflow.token_count}")
        return

    # Try execution
    execution = executor.get_execution(target)
    if execution:
        console.print(f"Execution: {execution.execution_id}")
        console.print(f"  Workflow: {execution.workflow_name}")
        console.print(f"  Status: {execution.status.value}")
        console.print(f"  Step: {execution.current_step}/{execution.steps_total}")
        return

    print_output(OutputType.ERROR, f"Not found: {target}")
    raise typer.Exit(4)
