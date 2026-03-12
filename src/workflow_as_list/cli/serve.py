"""workflow serve command - Start HTTP server (foreground mode)."""

import typer
from rich.console import Console

from ..constants import DEFAULT_HOST, DEFAULT_PORT
from ..models import OutputType

console = Console()


def print_output(type: OutputType, message: str):
    """Print formatted output with [TYPE] prefix."""
    console.print(f"[{type.value}] {message}")


def serve(
    host: str = typer.Option(DEFAULT_HOST, help="Host to bind"),
    port: int = typer.Option(DEFAULT_PORT, help="Port to bind"),
):
    """Start HTTP server (foreground mode)."""
    print_output(OutputType.INFO, f"Starting server on {host}:{port}")
    print_output(OutputType.NEXT, "Access API at http://localhost:8080/docs")

    # Import here to avoid circular dependency
    import uvicorn

    from ..server import create_app

    app_instance = create_app()
    uvicorn.run(app_instance, host=host, port=port)
