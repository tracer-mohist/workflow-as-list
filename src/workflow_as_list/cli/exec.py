"""workflow exec command - Execution instance management."""

from pathlib import Path

import typer
from rich.console import Console

from ..constants import ensure_directories
from ..executor import Executor, WorkflowParser
from ..models import OutputType

console = Console()


def print_output(type: OutputType, message: str):
    """Print formatted output with [TYPE] prefix."""
    console.print(f"[{type.value}] {message}")


app = typer.Typer(help="Execution instance management")


@app.command("show")
def exec_show(
    execution_id: str = typer.Argument(..., help="Execution instance ID"),
):
    """Show execution instance details.

    Example:
        workflow exec show commit-abc123
    """
    ensure_directories()
    executor = Executor()

    execution = executor.get_execution(execution_id)
    if not execution:
        print_output(OutputType.ERROR, f"Execution not found: {execution_id}")
        print_output(
            OutputType.NEXT, "List executions: ls ~/.workflow-as-list/executions/"
        )
        raise typer.Exit(4)

    console.print(f"Execution: {execution.execution_id}")
    console.print(f"  Workflow: {execution.workflow_name}")
    console.print(f"  Status: {execution.status.value}")
    console.print(f"  Step: {execution.current_step}/{execution.steps_total}")
    console.print(f"  Outputs: {execution.outputs_path}")


@app.command("next")
def exec_next(
    execution_id: str = typer.Argument(..., help="Execution instance ID"),
    output: str = typer.Option(None, "-o", "--output", help="Step output to store"),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Quiet mode (no output)"),
):
    """Mark current step complete and advance to next step.

    Shows current step content, stores output (if provided), advances execution,
    and displays next step content.

    Example:
        workflow exec next commit-abc123
        workflow exec next commit-abc123 -o "result"
        workflow exec next commit-abc123 -q  # Quiet mode for scripts
    """
    ensure_directories()
    executor = Executor()

    execution = executor.get_execution(execution_id)
    if not execution:
        print_output(OutputType.ERROR, f"Execution not found: {execution_id}")
        raise typer.Exit(4)

    # Load workflow and parse
    workflow = executor.get_workflow(execution.workflow_name)
    if not workflow:
        print_output(OutputType.ERROR, f"Workflow not found: {execution.workflow_name}")
        raise typer.Exit(4)

    content = Path(workflow.file_path).read_text()
    parser = WorkflowParser(content)
    parser.parse()

    # Get current step BEFORE advancing
    current_step = executor.get_next_step(execution, parser)

    # Show current step (unless quiet mode)
    if not quiet and current_step:
        console.print(
            f"[INFO] Current step {execution.current_step + 1}/{execution.steps_total}:"
        )
        console.print(f"  {current_step['content']}")
        if current_step.get("metadata"):
            for comment in current_step["metadata"][:3]:
                console.print(f"  {comment}")

    # Store output if provided
    if output:
        executor.store_output(execution_id, execution.current_step, output)

    # Advance execution
    executor.advance_execution(execution)

    # Get next step AFTER advancing
    next_step = executor.get_next_step(execution, parser)
    if next_step is None:
        print_output(OutputType.SUCCESS, f"Execution completed: {execution_id}")
        console.print(f"  Final step: {execution.steps_total}/{execution.steps_total}")
        return

    # Show next step (unless quiet mode)
    if not quiet:
        print_output(
            OutputType.SUCCESS,
            f"Advanced to step {execution.current_step}/{execution.steps_total}",
        )
        console.print(f"  Next step: {next_step['content']}")
        if next_step.get("metadata"):
            for comment in next_step["metadata"][:3]:
                console.print(f"  {comment}")
