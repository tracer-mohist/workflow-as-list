"""CLI entry point.

Re-exports app from cli package for backward compatibility.
"""

from .cli import app, main

__all__ = ["app", "main"]
