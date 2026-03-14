# src/workflow_as_list/cli/show.py
"""workflow show command - Show workflow definition details."""

from pathlib import Path

import typer
from rich.console import Console

from ..constants import ensure_directories
from ..executor import Executor, WorkflowLoader
from ..models import OutputType

console = Console()


def print_output(type: OutputType, message: str):
    """Print formatted output with [TYPE] prefix."""
    console.print(f"[{type.value}] {message}")


def show(
    name: str = typer.Argument(..., help="Workflow name to show"),
    expanded: bool = typer.Option(
        False, "--expanded", "-e", help="Show expanded content (imports inlined)"
    ),
):
    """Show workflow definition details.

    NOTE: For execution instances, use 'workflow exec <id> --show'
    """
    ensure_directories()
    executor = Executor()

    workflow = executor.get_workflow(name)
    if not workflow:
        print_output(OutputType.ERROR, f"Workflow not found: {name}")
        print_output(OutputType.NEXT, "List workflows: workflow list")
        raise typer.Exit(4)

    console.print(f"Workflow: {workflow.name}")
    console.print(f"  Status: {workflow.status.value}")
    console.print(f"  File: {workflow.file_path}")
    console.print(f"  Lines: {workflow.line_count}")
    console.print(f"  Tokens: {workflow.token_count}")

    if expanded:
        console.print("\n[INFO] Expanded content (imports inlined):")
        console.print("-" * 60)
        loader = WorkflowLoader(Path.cwd())
        expanded_content = loader.load(Path(workflow.file_path))
        console.print(expanded_content)
