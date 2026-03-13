"""CLI subcommands and main app for workflow-as-list.

Subcommands are defined in separate modules for maintainability.
This module assembles them into the main app.
"""

import typer

# Import subcommands
from .approve import approve
from .check import check
from .list import list_workflows
from .reject import reject
from .run import run
from .server import app as server_app
from .show import show

# Create main Typer app
app = typer.Typer(help="WorkflowAsList CLI - A thinking constraint DSL")

# Register all commands
app.command()(check)
app.command()(approve)
app.command()(reject)
app.command()(run)
app.command(name="list")(list_workflows)
app.command()(show)
app.add_typer(server_app, name="server")


def main():
    """CLI entry point."""
    app()


__all__ = [
    "app",
    "main",
    "approve",
    "check",
    "list_workflows",
    "reject",
    "run",
    "show",
    "server_app",
]
