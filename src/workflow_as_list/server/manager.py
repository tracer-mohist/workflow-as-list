# src/workflow_as_list/server/manager.py
"""Server lifecycle management.

Manages the uvicorn server process: start, stop, status, and logs.
"""

import os
import signal
import subprocess
import sys
from pathlib import Path

from ..constants import (
    DEFAULT_HOST,
    DEFAULT_PORT,
    PID_FILE,
    SERVER_LOG,
    ensure_directories,
)


def is_running() -> bool:
    """Check if server is currently running.

    Returns:
        True if server process is alive, False otherwise.
    """
    if not PID_FILE.exists():
        return False

    try:
        pid = int(PID_FILE.read_text().strip())
        # Check if process exists
        os.kill(pid, 0)
        return True
    except (ValueError, ProcessLookupError, PermissionError):
        # PID file exists but process is dead
        # Clean up stale PID file
        PID_FILE.unlink(missing_ok=True)
        return False


def get_pid() -> int | None:
    """Get current server PID if running.

    Returns:
        PID if server is running, None otherwise.
    """
    if not PID_FILE.exists():
        return None

    try:
        return int(PID_FILE.read_text().strip())
    except ValueError:
        return None


def start(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> bool:
    """Start the uvicorn server.

    Args:
        host: Host to bind to (default: 127.0.0.1)
        port: Port to bind to (default: 8080)

    Returns:
        True if server started successfully, False if already running.
    """
    if is_running():
        pid = get_pid()
        print(f"Server already running (PID: {pid})")
        return False

    # Ensure directories exist
    ensure_directories()

    # Start uvicorn as subprocess
    # Log to SERVER_LOG, run in background
    log_file = open(SERVER_LOG, "a")

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "workflow_as_list.server:app",
        "--host",
        host,
        "--port",
        str(port),
    ]

    process = subprocess.Popen(
        cmd,
        stdout=log_file,
        stderr=log_file,
        start_new_session=True,  # Create new process group
        cwd=str(Path(__file__).parent.parent.parent),  # Package root
    )

    # Write PID file
    PID_FILE.write_text(str(process.pid))

    print(f"Server started on {host}:{port} (PID: {process.pid})")
    print(f"Logs: {SERVER_LOG}")

    return True


def stop() -> bool:
    """Stop the uvicorn server.

    Sends SIGTERM to the server process and cleans up PID file.

    Returns:
        True if server stopped successfully, False if not running.
    """
    if not is_running():
        print("Server not running")
        return False

    pid = get_pid()
    if pid is None:
        print("Server not running (no PID)")
        return False

    try:
        # Send SIGTERM
        os.kill(pid, signal.SIGTERM)
        print(f"Server stopped (PID: {pid})")
    except ProcessLookupError:
        print("Server process not found (already stopped?)")
    except PermissionError:
        print(f"Permission denied to stop process {pid}")
        return False
    finally:
        # Cleanup PID file
        PID_FILE.unlink(missing_ok=True)

    return True


def status() -> dict:
    """Get server status.

    Returns:
        Dictionary with status information:
        - running: bool
        - pid: int | None
        - host: str | None
        - port: int | None
    """
    running = is_running()
    pid = get_pid() if running else None

    return {
        "running": running,
        "pid": pid,
        "host": DEFAULT_HOST,
        "port": DEFAULT_PORT,
    }


def logs(lines: int = 50, follow: bool = False) -> None:
    """View server logs.

    Args:
        lines: Number of lines to show (default: 50)
        follow: If True, follow logs (like tail -f)
    """
    if not SERVER_LOG.exists():
        print("No logs found")
        return

    if follow:
        # Follow mode - use subprocess to tail -f
        subprocess.run(["tail", "-f", str(SERVER_LOG)])
    else:
        # Show last N lines
        content = SERVER_LOG.read_text()
        all_lines = content.splitlines()
        recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines

        for line in recent_lines:
            print(line)


def print_status() -> None:
    """Print human-readable server status."""
    info = status()

    if info["running"]:
        print(f"[OK] Server running (PID: {info['pid']})")
        print(f"  Host: {info['host']}")
        print(f"  Port: {info['port']}")
        print(f"  URL: http://{info['host']}:{info['port']}")
        print(f"  API: http://{info['host']}:{info['port']}/docs")
    else:
        print("[NO] Server not running")
        print("  Start with: workflow server start")
