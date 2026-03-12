"""workflow run command - Execute workflows."""

from pathlib import Path

import typer
from rich.console import Console

from ..config import load_config
from ..constants import ensure_directories
from ..executor import Executor, WorkflowParser
from ..models import AuditStatus, OutputType

console = Console()


def print_output(type: OutputType, message: str):
    """Print formatted output with [TYPE] prefix."""
    console.print(f"[{type.value}] {message}")


def run(name: str = typer.Argument(..., help="Workflow name to execute")):
    """Execute a workflow."""
    ensure_directories()
    config = load_config()
    executor = Executor(config)

    workflow = executor.get_workflow(name)
    if not workflow:
        print_output(OutputType.ERROR, f"Workflow not found: {name}")
        raise typer.Exit(4)

    if workflow.status != AuditStatus.APPROVED:
        print_output(
            OutputType.ERROR,
            f"Workflow not approved: {name} (status: {workflow.status.value})",
        )
        print_output(OutputType.NEXT, f"Run: workflow approve {name}")
        raise typer.Exit(5)

    # Read and parse workflow
    content = Path(workflow.file_path).read_text()
    parser = WorkflowParser(content)
    steps = parser.parse()

    # Create execution
    execution = executor.create_execution(workflow, len(steps))

    print_output(OutputType.SUCCESS, f"Execution started: {execution.execution_id}")
    print_output(OutputType.INFO, f"Total steps: {execution.steps_total}")
    print_output(OutputType.NEXT, f"Monitor: workflow show {execution.execution_id}")
