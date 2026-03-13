# tests/test_execution_workflow_e2e.py
"""E2E tests for execution workflow with progressive reading.

REFERENCE: principles/automation/testing-strategy.md
- Tests business-impacting workflows only
- 5-15 E2E tests maximum
"""

import tempfile
from pathlib import Path

from typer.testing import CliRunner

from workflow_as_list.cli import app
from workflow_as_list.constants import ensure_directories

runner = CliRunner()


def test_complete_execution_workflow():
    """Scenario: User completes full execution workflow with progressive reading.
    Expected: Can read steps, advance only after reading, complete workflow.
    If fails: Progressive reading model broken, core value proposition compromised.
    """
    ensure_directories()

    # Create test workflow with unique name
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".workflow.list", delete=False, prefix="test_"
    ) as f:
        f.write("# Test workflow\n- (start) Step 1\n- Step 2\n- End\n")
        f.flush()
        workflow_path = Path(f.name)

    # Workflow name is derived from filename (remove .workflow.list suffix)
    # e.g., test_abc.workflow.list -> test_abc.workflow
    workflow_name = workflow_path.stem

    try:
        # Check and approve
        result = runner.invoke(app, ["check", str(workflow_path)])
        assert result.exit_code == 0

        result = runner.invoke(app, ["approve", workflow_name])
        assert result.exit_code == 0

        # Run to create execution
        result = runner.invoke(app, ["run", workflow_name])
        assert result.exit_code == 0

        # Extract execution ID
        import re

        pattern = rf"Execution started: ({workflow_name}-\w+)"
        match = re.search(pattern, result.output)
        assert match, f"Could not find execution ID: {result.output}"
        execution_id = match.group(1)

        # Progressive reading: read → next → read → next
        for step_num in range(1, 4):
            # Read
            result = runner.invoke(app, ["exec", "read", execution_id])
            assert result.exit_code == 0, (
                f"Read step {step_num} failed: {result.output}"
            )

            # Next
            result = runner.invoke(app, ["exec", "next", execution_id])
            if step_num < 3:
                assert result.exit_code == 0, (
                    f"Next step {step_num} failed: {result.output}"
                )
            else:
                # Last step should complete
                assert "completed" in result.output.lower()

    finally:
        workflow_path.unlink()
