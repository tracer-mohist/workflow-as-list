# tests/test_audit_workflow_e2e.py
"""E2E tests for audit workflow.

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


def test_complete_audit_workflow():
    """Scenario: User completes full audit workflow (check → approve → reject).
    Expected: Workflow can be approved and rejected.
    If fails: Audit workflow broken, security model compromised.
    """
    ensure_directories()

    # Create test workflow with unique name
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".workflow.list", delete=False, prefix="test_"
    ) as f:
        f.write("# Test workflow\n- (start) Test\n- End\n")
        f.flush()
        workflow_path = Path(f.name)

    # Workflow name is derived from filename (remove .workflow.list suffix)
    # e.g., test_abc.workflow.list -> test_abc.workflow
    workflow_name = workflow_path.stem

    try:
        # Check
        result = runner.invoke(app, ["check", str(workflow_path)])
        assert result.exit_code == 0, f"Check failed: {result.output}"
        assert "Workflow registered" in result.output

        # Approve
        result = runner.invoke(app, ["approve", workflow_name])
        assert result.exit_code == 0, f"Approve failed: {result.output}"
        assert "approved" in result.output.lower()

        # Reject (to test reject flow)
        result = runner.invoke(app, ["reject", workflow_name])
        assert result.exit_code == 0, f"Reject failed: {result.output}"
        assert "rejected" in result.output.lower()

    finally:
        workflow_path.unlink()
