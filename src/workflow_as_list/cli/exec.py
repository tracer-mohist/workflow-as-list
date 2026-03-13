"""workflow exec command - Execution instance management."""

import typer
from rich.console import Console

from ..constants import ensure_directories
from ..executor import Executor
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
):
    """Mark current step complete and advance to next step.

    Example:
        workflow exec next commit-abc123
        workflow exec next commit-abc123 -o "result"
    """
    ensure_directories()
    executor = Executor()

    execution = executor.get_execution(execution_id)
    if not execution:
        print_output(OutputType.ERROR, f"Execution not found: {execution_id}")
        raise typer.Exit(4)

    # Store output if provided
    if output:
        executor.store_output(execution_id, execution.current_step, output)

    # Advance execution
    executor.advance_execution(execution)

    # Get next step
    from ..executor import WorkflowParser

    workflow = executor.get_workflow(execution.workflow_name)
    if not workflow:
        print_output(OutputType.ERROR, f"Workflow not found: {execution.workflow_name}")
        raise typer.Exit(4)

    content = executor.__class__.__module__.replace(
        "executor.state", "workflow_as_list"
    )
    from pathlib import Path

    content = Path(workflow.file_path).read_text()
    parser = WorkflowParser(content)
    parser.parse()

    next_step = executor.get_next_step(execution, parser)
    if next_step is None:
        print_output(OutputType.SUCCESS, f"Execution completed: {execution_id}")
        console.print(f"  Final step: {execution.steps_total}/{execution.steps_total}")
        return

    print_output(
        OutputType.SUCCESS,
        f"Advanced to step {execution.current_step + 1}/{execution.steps_total}",
    )
    console.print(f"  Next step: {next_step['content']}")
    if next_step.get("metadata"):
        console.print(f"  Metadata: {len(next_step['metadata'])} comments")
