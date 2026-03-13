# src/workflow_as_list/cli/server.py
"""workflow server command - Server lifecycle management."""

import typer
from rich.console import Console

from ..constants import DEFAULT_HOST, DEFAULT_PORT
from ..models import OutputType
from ..server.manager import logs, print_status, start, stop

console = Console()


def print_output(type: OutputType, message: str):
    """Print formatted output with [TYPE] prefix."""
    console.print(f"[{type.value}] {message}")


# Create Typer app for server subcommands
app = typer.Typer(help="Server lifecycle management")


@app.command("start")
def server_start(
    host: str = typer.Option(DEFAULT_HOST, help="Host to bind"),
    port: int = typer.Option(DEFAULT_PORT, help="Port to bind"),
):
    """Start the server in background mode."""
    success = start(host, port)
    if success:
        print_output(OutputType.SUCCESS, "Server started")
        print_output(OutputType.NEXT, "Check status: workflow server status")
        print_output(OutputType.NEXT, "View logs: workflow server logs")
        print_output(OutputType.NEXT, "Stop server: workflow server stop")
    else:
        raise typer.Exit(1)


@app.command("stop")
def server_stop():
    """Stop the server."""
    success = stop()
    if success:
        print_output(OutputType.SUCCESS, "Server stopped")
    else:
        raise typer.Exit(1)


@app.command("status")
def server_status():
    """Check server status."""
    print_status()


@app.command("logs")
def server_logs(
    lines: int = typer.Option(50, help="Number of lines to show"),
    follow: bool = typer.Option(False, "-f", "--follow", help="Follow logs"),
):
    """View server logs."""
    logs(lines=lines, follow=follow)
