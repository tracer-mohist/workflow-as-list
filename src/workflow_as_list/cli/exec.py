# src/workflow_as_list/cli/exec.py
"""workflow exec command - Execution instance management for progressive reading.

Design:
- read: Read current step content (mark as read)
- next: Advance to next step (must read first)

Progressive reading ensures Agent cannot skip steps without reading.
"""

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


app = typer.Typer(help="Execution instance management (progressive reading)")


@app.command("read")
def exec_read(
    execution_id: str = typer.Argument(..., help="Execution instance ID"),
):
    """Read current step content and mark as read.

    Agent reads the current step, understands it, then executes operations
    using its own tools (git, file operations, API calls, etc.).

    After reading and executing, call 'workflow exec next' to advance.

    Example:
        workflow exec read commit-abc123
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

    # Load workflow and parse
    workflow = executor.get_workflow(execution.workflow_name)
    if not workflow:
        print_output(OutputType.ERROR, f"Workflow not found: {execution.workflow_name}")
        raise typer.Exit(4)

    content = Path(workflow.file_path).read_text()
    parser = WorkflowParser(content)
    parser.parse()

    # Get current step
    current_step = executor.get_next_step(execution, parser)
    if current_step is None:
        print_output(OutputType.SUCCESS, f"Execution completed: {execution_id}")
        console.print(f"  All {execution.steps_total} steps completed")
        return

    # Display current step content
    console.print(f"[INFO] Step {execution.current_step + 1}/{execution.steps_total}:")
    console.print(f"  {current_step['content']}")
    if current_step.get("metadata"):
        console.print(f"  Comments ({len(current_step['metadata'])}):")
        for comment in current_step["metadata"]:
            console.print(f"    {comment}")

    # Mark as read (if not already)
    if execution.current_step not in execution.steps_read:
        execution.steps_read.append(execution.current_step)
        executor.update_execution(execution)
        console.print(f"\n[INFO] Step {execution.current_step + 1} marked as read")


@app.command("next")
def exec_next(
    execution_id: str = typer.Argument(..., help="Execution instance ID"),
):
    """Advance to next step (must read current step first).

    Checks if current step has been read (progressive reading enforcement).
    If read, advances to next step. If not read, shows error.

    Agent should:
    1. workflow exec read <id> (read and understand)
    2. Execute operations (using own tools)
    3. workflow exec next <id> (advance when ready)

    Example:
        workflow exec next commit-abc123
    """
    ensure_directories()
    executor = Executor()

    execution = executor.get_execution(execution_id)
    if not execution:
        print_output(OutputType.ERROR, f"Execution not found: {execution_id}")
        raise typer.Exit(4)

    # Check if current step has been read
    if execution.current_step not in execution.steps_read:
        print_output(OutputType.ERROR, "Current step not read yet")
        print_output(
            OutputType.NEXT,
            f"Read first: workflow exec read {execution_id}",
        )
        raise typer.Exit(1)

    # Advance execution
    executor.advance_execution(execution)

    # Check if completed
    workflow = executor.get_workflow(execution.workflow_name)
    if not workflow:
        print_output(OutputType.ERROR, f"Workflow not found: {execution.workflow_name}")
        raise typer.Exit(4)

    content = Path(workflow.file_path).read_text()
    parser = WorkflowParser(content)
    parser.parse()

    next_step = executor.get_next_step(execution, parser)
    if next_step is None:
        print_output(OutputType.SUCCESS, f"Execution completed: {execution_id}")
        console.print(f"  Total steps: {execution.steps_total}")
        return

    # Show progress (not content - Agent reads with 'read' command)
    print_output(
        OutputType.SUCCESS,
        f"Advanced to step {execution.current_step + 1}/{execution.steps_total}",
    )
    console.print(f"  Read next: workflow exec read {execution_id}")
