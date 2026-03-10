# src/workflow_as_list/cli.py
"""CLI interface using Typer.

7 subcommands: check, approve, reject, run, list, show, serve
"""

from pathlib import Path

import typer
from rich.console import Console

from .config import ensure_config_dir, load_config
from .executor import Executor, WorkflowParser
from .models import AuditStatus, OutputType
from .security import compute_hash, run_security_checks

app = typer.Typer(help="WorkflowAsList CLI - A thinking constraint DSL")
console = Console()


def print_output(type: OutputType, message: str):
    """Print formatted output with [TYPE] prefix."""
    console.print(f"[{type.value}] {message}")


@app.command()
def check(
    file: Path = typer.Argument(..., help="Workflow file to validate and register"),
):
    """Validate and register a workflow file."""
    config = load_config()
    config_dir = ensure_config_dir(config)
    executor = Executor(config_dir)

    # Read file
    if not file.exists():
        print_output(OutputType.ERROR, f"File not found: {file}")
        raise typer.Exit(1)

    content = file.read_text()
    file_hash = compute_hash(file)

    # Run security checks (skip Layer 5 - audit status check)
    passed, errors = run_security_checks(
        content, config, "pending_audit", skip_audit_check=True
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


@app.command()
def approve(name: str = typer.Argument(..., help="Workflow name to approve")):
    """Approve a workflow for execution."""
    config = load_config()
    config_dir = ensure_config_dir(config)
    executor = Executor(config_dir)

    workflow = executor.get_workflow(name)
    if not workflow:
        print_output(OutputType.ERROR, f"Workflow not found: {name}")
        raise typer.Exit(4)

    if workflow.status == AuditStatus.APPROVED:
        print_output(OutputType.WARN, f"Workflow already approved: {name}")
        return

    executor.update_workflow_status(name, AuditStatus.APPROVED)
    print_output(OutputType.SUCCESS, f"Workflow approved: {name}")
    print_output(OutputType.NEXT, f"Run: workflow run {name}")


@app.command()
def reject(name: str = typer.Argument(..., help="Workflow name to reject")):
    """Reject a workflow."""
    config = load_config()
    config_dir = ensure_config_dir(config)
    executor = Executor(config_dir)

    workflow = executor.get_workflow(name)
    if not workflow:
        print_output(OutputType.ERROR, f"Workflow not found: {name}")
        raise typer.Exit(4)

    executor.update_workflow_status(name, AuditStatus.REJECTED)
    print_output(OutputType.SUCCESS, f"Workflow rejected: {name}")


@app.command()
def run(name: str = typer.Argument(..., help="Workflow name to execute")):
    """Execute a workflow."""
    config = load_config()
    config_dir = ensure_config_dir(config)
    executor = Executor(config_dir)

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


@app.command()
def list():
    """List all registered workflows."""
    config = load_config()
    config_dir = ensure_config_dir(config)
    executor = Executor(config_dir)

    workflows = executor.list_workflows()

    if not workflows:
        print_output(OutputType.INFO, "No workflows registered")
        return

    print_output(OutputType.INFO, f"Registered workflows: {len(workflows)}")
    for wf in workflows:
        status_icon = "✓" if wf.status == AuditStatus.APPROVED else "○"
        console.print(f"  {status_icon} {wf.name} ({wf.status.value})")


@app.command()
def show(target: str = typer.Argument(..., help="Workflow name or execution ID")):
    """Show workflow or execution details."""
    config = load_config()
    config_dir = ensure_config_dir(config)
    executor = Executor(config_dir)

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


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Host to bind"),
    port: int = typer.Option(8080, help="Port to bind"),
):
    """Start HTTP server."""
    print_output(OutputType.INFO, f"Starting server on {host}:{port}")
    print_output(OutputType.NEXT, "Access API at http://localhost:8080/docs")

    # Import here to avoid circular dependency
    import uvicorn

    from .server import create_app

    app_instance = create_app()
    uvicorn.run(app_instance, host=host, port=port)


def main():
    """CLI entry point."""
    app()


if __name__ == "__main__":
    main()
