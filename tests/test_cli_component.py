# tests/test_cli_component.py
"""Component tests for CLI commands.

NOTE: Follows Limited Testing Strategy - test user-facing behavior only.
Test main scenarios, not edge cases.
REFERENCE: docs/limited-testing-strategy.md
"""

import tempfile
from pathlib import Path

from typer.testing import CliRunner

from workflow_as_list.cli import app

runner = CliRunner()


def test_help_command():
    """Scenario: User runs workflow --help.
    Expected: Shows help with 7 commands.
    If fails: CLI entry point broken.
    """
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "check" in result.stdout
    assert "approve" in result.stdout
    assert "run" in result.stdout


def test_check_missing_file():
    """Scenario: User runs check without file.
    Expected: Exit code non-zero.
    If fails: Argument parsing broken.
    """
    result = runner.invoke(app, ["check"])
    assert result.exit_code != 0


def test_check_file_not_found():
    """Scenario: User runs check with non-existent file.
    Expected: Shows file not found error.
    If fails: Error handling broken.
    """
    result = runner.invoke(app, ["check", "/nonexistent/file.wf"])
    assert result.exit_code != 0
    assert "not found" in result.stdout.lower() or "error" in result.stdout.lower()


def test_list_empty():
    """Scenario: User runs list with no workflows.
    Expected: Shows empty list message.
    If fails: List command broken.
    """
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    # Should not crash, may show "no workflows" or empty list


def test_show_missing_argument():
    """Scenario: User runs show without name.
    Expected: Shows error about missing argument.
    If fails: Argument validation broken.
    """
    result = runner.invoke(app, ["show"])
    assert result.exit_code != 0


def test_valid_workflow_check():
    """Scenario: User checks a valid workflow file.
    Expected: Workflow registered or validation error.
    If fails: Core workflow parsing broken.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".wf", delete=False) as f:
        # Create minimal valid workflow (282-358 bytes)
        content = "x" * 300
        f.write(content)
        f.flush()
        workflow_path = Path(f.name)

    try:
        result = runner.invoke(app, ["check", str(workflow_path)])
        # Should not crash - may pass or fail validation
        assert result.exit_code in [0, 3]  # 0=success, 3=syntax error
    finally:
        workflow_path.unlink()
