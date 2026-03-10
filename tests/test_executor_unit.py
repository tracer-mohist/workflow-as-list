# tests/test_executor_unit.py
"""Unit tests for executor module.

NOTE: Follows Limited Testing Strategy - test critical logic only.
REFERENCE: docs/limited-testing-strategy.md
REFERENCE: docs/design/runtime/007-execution.md
"""

import tempfile
from pathlib import Path

from workflow_as_list.executor import Executor, WorkflowParser
from workflow_as_list.models import AuditStatus


class TestWorkflowParser:
    """WorkflowParser unit tests."""

    def test_parse_simple_content(self):
        """Scenario: Parse simple workflow with content lines.
        Expected: Steps extracted correctly.
        If fails: Basic parsing broken.
        """
        content = """First step
Second step
Third step"""
        parser = WorkflowParser(content)
        steps = parser.parse()
        assert len(steps) == 3
        assert steps[0]["content"] == "First step"
        assert steps[1]["content"] == "Second step"

    def test_parse_tagged_lines(self):
        """Scenario: Parse workflow with tags.
        Expected: Tags extracted and indexed.
        If fails: Tag-based jumps broken.
        """
        content = """(start) First step
(middle) Second step
(end) Third step"""
        parser = WorkflowParser(content)
        steps = parser.parse()
        assert len(steps) == 3
        assert "start" in parser.tags
        assert "middle" in parser.tags
        assert "end" in parser.tags

    def test_parse_jump_lines(self):
        """Scenario: Parse workflow with jump instructions.
        Expected: Jump target, limit, condition extracted.
        If fails: Jump logic broken.
        """
        content = """(start) First step
@start[3]: if condition
Second step"""
        parser = WorkflowParser(content)
        steps = parser.parse()
        jump_step = steps[1]
        assert jump_step["jump_target"] == "start"
        assert jump_step["jump_limit"] == 3
        assert jump_step["jump_condition"] == "if condition"

    def test_parse_nested_content(self):
        """Scenario: Parse workflow with indentation.
        Expected: Indent level detected.
        If fails: Sub-task detection broken.
        """
        content = """Parent step
  Child step
  Another child"""
        parser = WorkflowParser(content)
        steps = parser.parse()
        assert steps[0]["indent"] == 0
        assert steps[1]["indent"] == 2
        assert steps[2]["indent"] == 2

    def test_parse_import_directive(self):
        """Scenario: Parse workflow with import.
        Expected: Import path extracted.
        If fails: Workflow composition broken.
        """
        content = """First step
import: other.wf
Last step"""
        parser = WorkflowParser(content)
        parser.parse()
        assert len(parser.imports) == 1
        assert parser.imports[0] == "other.wf"


class TestExecutor:
    """Executor unit tests."""

    def _create_executor(self):
        """Helper: Create executor with temp directory."""
        temp_dir = Path(tempfile.mkdtemp())
        return Executor(temp_dir), temp_dir

    def test_register_workflow(self):
        """Scenario: Register new workflow.
        Expected: Workflow added to registry.jsonl.
        If fails: Workflow registration broken.
        """
        executor, temp_dir = self._create_executor()
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".wf") as f:
            f.write("test content")
            f.flush()
            file_path = Path(f.name)

        workflow = executor.register_workflow(
            name="test_wf",
            file_path=file_path,
            content="test content",
            file_hash="abc123",
            token_count=100,
        )

        assert workflow.name == "test_wf"
        assert workflow.status == AuditStatus.PENDING_AUDIT
        assert executor.registry_path.exists()

    def test_get_workflow(self):
        """Scenario: Retrieve registered workflow by name.
        Expected: Returns Workflow object.
        If fails: Workflow lookup broken.
        """
        executor, temp_dir = self._create_executor()
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".wf") as f:
            f.write("test content")
            f.flush()
            file_path = Path(f.name)

        executor.register_workflow(
            name="test_wf",
            file_path=file_path,
            content="test content",
            file_hash="abc123",
            token_count=100,
        )

        workflow = executor.get_workflow("test_wf")
        assert workflow is not None
        assert workflow.name == "test_wf"

    def test_update_workflow_status(self):
        """Scenario: Update workflow from PENDING to APPROVED.
        Expected: Status changed in registry.
        If fails: Audit workflow broken.
        """
        executor, temp_dir = self._create_executor()
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".wf") as f:
            f.write("test content")
            f.flush()
            file_path = Path(f.name)

        executor.register_workflow(
            name="test_wf",
            file_path=file_path,
            content="test content",
            file_hash="abc123",
            token_count=100,
        )

        success = executor.update_workflow_status("test_wf", AuditStatus.APPROVED)
        assert success is True

        workflow = executor.get_workflow("test_wf")
        assert workflow.status == AuditStatus.APPROVED

    def test_create_execution(self):
        """Scenario: Create execution instance for workflow.
        Expected: Execution file created in executions/.
        If fails: Execution tracking broken.
        """
        executor, temp_dir = self._create_executor()
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".wf") as f:
            f.write("test content")
            f.flush()
            file_path = Path(f.name)

        workflow = executor.register_workflow(
            name="test_wf",
            file_path=file_path,
            content="test content",
            file_hash="abc123",
            token_count=100,
        )

        execution = executor.create_execution(workflow, steps_total=5)
        assert execution.workflow_name == "test_wf"
        assert execution.steps_total == 5
        assert execution.current_step == 0

        # Check execution file exists
        execution_file = executor.executions_dir / f"{execution.execution_id}.json"
        assert execution_file.exists()

    def test_advance_execution(self):
        """Scenario: Advance execution to next step.
        Expected: current_step incremented.
        If fails: Step progression broken.
        """
        executor, temp_dir = self._create_executor()
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".wf") as f:
            f.write("test content")
            f.flush()
            file_path = Path(f.name)

        workflow = executor.register_workflow(
            name="test_wf",
            file_path=file_path,
            content="test content",
            file_hash="abc123",
            token_count=100,
        )

        execution = executor.create_execution(workflow, steps_total=5)
        assert execution.current_step == 0

        executor.advance_execution(execution)
        assert execution.current_step == 1

    def test_get_next_step(self):
        """Scenario: Get next step for Agent.
        Expected: Returns step dict or None if complete.
        If fails: Progressive exposure broken.
        """
        executor, temp_dir = self._create_executor()
        content = "Step 1\nStep 2\nStep 3"
        parser = WorkflowParser(content)
        parser.parse()

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".wf") as f:
            f.write(content)
            f.flush()
            file_path = Path(f.name)

        workflow = executor.register_workflow(
            name="test_wf",
            file_path=file_path,
            content=content,
            file_hash="abc123",
            token_count=len(content),
        )

        execution = executor.create_execution(workflow, steps_total=3)

        # Get first step
        step = executor.get_next_step(execution, parser)
        assert step is not None
        assert step["content"] == "Step 1"

        # Advance and get second step
        executor.advance_execution(execution)
        step = executor.get_next_step(execution, parser)
        assert step is not None
        assert step["content"] == "Step 2"

    def test_store_output(self):
        """Scenario: Store Agent output for a step.
        Expected: Output file created in outputs/.
        If fails: Output persistence broken.
        """
        executor, temp_dir = self._create_executor()
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".wf") as f:
            f.write("test content")
            f.flush()
            file_path = Path(f.name)

        workflow = executor.register_workflow(
            name="test_wf",
            file_path=file_path,
            content="test content",
            file_hash="abc123",
            token_count=100,
        )

        execution = executor.create_execution(workflow, steps_total=5)
        executor.store_output(execution.execution_id, 0, "Agent response for step 0")

        output_file = executor.outputs_dir / execution.execution_id / "0.txt"
        assert output_file.exists()
        assert output_file.read_text() == "Agent response for step 0"
