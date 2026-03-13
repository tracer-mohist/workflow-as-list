# tests/test_pipeline_integration.py
"""Integration tests for critical data flows.

REFERENCE: principles/automation/testing-strategy.md
- Tests real integration points, not hypothetical combinations
- Verifies necessary conditions, not sufficient conditions
"""

import tempfile
import uuid
from pathlib import Path

from typer.testing import CliRunner

from workflow_as_list.cli import app
from workflow_as_list.constants import ensure_directories

runner = CliRunner()


def test_check_approve_run_pipeline():
    """Scenario: User completes full workflow pipeline (check → approve → run).
    Expected: Workflow registered, approved, execution created.
    If fails: Core user workflow broken.
    """
    ensure_directories()

    # Use unique workflow name
    workflow_name = f"test_{uuid.uuid4().hex[:8]}"

    # Create test workflow
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".workflow.list", delete=False
    ) as f:
        f.write(f"- (start) Test {workflow_name}\n- End\n")
        f.flush()
        workflow_path = Path(f.name)

    try:
        # Workflow name is derived from filename (remove .workflow.list suffix)
        # e.g., test_abc.workflow.list -> test_abc.workflow
        workflow_name = workflow_path.stem

        # Check
        result = runner.invoke(app, ["check", str(workflow_path)])
        assert result.exit_code == 0, f"Check failed: {result.output}"

        # Approve
        result = runner.invoke(app, ["approve", workflow_name])
        assert result.exit_code == 0, f"Approve failed: {result.output}"

        # Run
        result = runner.invoke(app, ["run", workflow_name])
        assert result.exit_code == 0, f"Run failed: {result.output}"
        assert "Execution started" in result.output

    finally:
        workflow_path.unlink()


def test_exec_read_next_pipeline():
    """Scenario: User uses progressive reading (read → next).
    Expected: Can read step, advance only after reading.
    If fails: Progressive reading enforcement broken.
    """
    ensure_directories()

    # Create test workflow with unique name
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".workflow.list", delete=False, prefix="test_"
    ) as f:
        f.write("- (start) Step 1\n- Step 2\n- End\n")
        f.flush()
        workflow_path = Path(f.name)

    # Workflow name is derived from filename (remove .workflow.list suffix)
    # e.g., test_abc.workflow.list -> test_abc.workflow
    workflow_name = workflow_path.stem

    try:
        # Check and approve
        runner.invoke(app, ["check", str(workflow_path)])
        runner.invoke(app, ["approve", workflow_name])

        # Run to create execution
        result = runner.invoke(app, ["run", workflow_name])
        assert result.exit_code == 0

        # Extract execution ID from output
        # Format: "Execution started: test_abc.workflow-xyz"
        import re

        pattern = rf"Execution started: ({workflow_name}-\w+)"
        match = re.search(pattern, result.output)
        assert match, f"Could not find execution ID: {result.output}"
        execution_id = match.group(1)

        # Read current step
        result = runner.invoke(app, ["exec", "read", execution_id])
        assert result.exit_code == 0, f"Read failed: {result.output}"
        assert "Step 1" in result.output

        # Next should succeed (step was read)
        result = runner.invoke(app, ["exec", "next", execution_id])
        assert result.exit_code == 0, f"Next failed: {result.output}"
        assert "Advanced to step" in result.output

        # Try next again (should fail - step 2 not read)
        result = runner.invoke(app, ["exec", "next", execution_id])
        assert result.exit_code != 0, "Next should fail without reading first"
        assert "not read" in result.output.lower()

    finally:
        workflow_path.unlink()
