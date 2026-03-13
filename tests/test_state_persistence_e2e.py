# tests/test_state_persistence_e2e.py
"""E2E tests for state persistence.

REFERENCE: principles/automation/testing-strategy.md
- Tests business-impacting workflows only
- 5-15 E2E tests maximum
"""

import tempfile
from pathlib import Path

from typer.testing import CliRunner

from workflow_as_list.cli import app
from workflow_as_list.constants import ensure_directories
from workflow_as_list.executor import Executor

runner = CliRunner()


def test_state_persistence_after_restart():
    """Scenario: Execution state persists after "restart" (new Executor instance).
    Expected: Can resume execution from saved state.
    If fails: State persistence broken, cannot resume interrupted executions.
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
        runner.invoke(app, ["check", str(workflow_path)])
        runner.invoke(app, ["approve", workflow_name])

        # Run to create execution
        result = runner.invoke(app, ["run", workflow_name])
        assert result.exit_code == 0

        # Extract execution ID
        import re

        pattern = rf"Execution started: ({workflow_name}-\w+)"
        match = re.search(pattern, result.output)
        assert match, f"Could not find execution ID: {result.output}"
        execution_id = match.group(1)

        # Read step 1
        result = runner.invoke(app, ["exec", "read", execution_id])
        assert result.exit_code == 0

        # "Restart" - create new Executor instance
        executor = Executor()

        # Verify state persisted
        execution = executor.get_execution(execution_id)
        assert execution is not None, "Execution state not persisted"
        assert execution.workflow_name == workflow_name
        assert execution.steps_total == 3

        # Can continue from saved state
        result = runner.invoke(app, ["exec", "next", execution_id])
        assert result.exit_code == 0, f"Next after restart failed: {result.output}"

    finally:
        workflow_path.unlink()
