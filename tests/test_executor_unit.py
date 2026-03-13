# tests/test_executor_unit.py
"""Unit tests for executor module."""

import tempfile
from pathlib import Path

from workflow_as_list.executor import Executor, WorkflowParser
from workflow_as_list.models import AuditStatus


class TestWorkflowParser:
    """WorkflowParser unit tests."""

    def test_parse_simple_content(self):
        content = "- First step\n- Second step\n- Third step"
        parser = WorkflowParser(content)
        steps = parser.parse()
        assert len(steps) == 3
        assert steps[0]["content"] == "First step"
        assert steps[0]["metadata"] == []

    def test_parse_tagged_lines(self):
        content = "- (start) First step\n- (middle) Second step\n- (end) Third step"
        parser = WorkflowParser(content)
        steps = parser.parse()
        assert len(steps) == 3
        assert "start" in parser.tags
        assert "middle" in parser.tags

    def test_parse_jump_lines(self):
        content = "- (start) First step\n- @start[3]: if condition\n- Second step"
        parser = WorkflowParser(content)
        steps = parser.parse()
        jump_step = steps[1]
        assert jump_step["jump_target"] == "start"
        assert jump_step["jump_limit"] == 3

    def test_parse_nested_content(self):
        content = "- Parent step\n  - Child step\n  - Another child"
        parser = WorkflowParser(content)
        steps = parser.parse()
        assert len(steps) == 3
        assert steps[0]["indent"] == 0
        assert steps[1]["indent"] == 2

    def test_parse_import_directive(self):
        content = "- First step\n- import: other.wf\n- Last step"
        parser = WorkflowParser(content)
        parser.parse()
        assert len(parser.imports) == 1
        assert parser.imports[0] == "other.wf"


class TestExecutor:
    """Executor unit tests."""

    def _create_executor(self):
        temp_dir = tempfile.mkdtemp()
        return Executor(Path(temp_dir)), temp_dir

    def test_register_workflow(self):
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
        assert workflow is not None
        assert workflow.name == "test_wf"

    def test_get_workflow(self):
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

    def test_update_workflow_status(self):
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
        executor.update_workflow_status("test_wf", AuditStatus.APPROVED)
        workflow = executor.get_workflow("test_wf")
        assert workflow.status == AuditStatus.APPROVED

    def test_create_execution(self):
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

    def test_advance_execution(self):
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
        executor.advance_execution(execution)
        assert execution.current_step == 1

    def test_get_next_step(self):
        executor, temp_dir = self._create_executor()
        content = "- Step 1\n- Step 2\n- Step 3"
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
            token_count=100,
        )
        execution = executor.create_execution(workflow, steps_total=3)
        step = executor.get_next_step(execution, parser)
        assert step is not None
        assert step["content"] == "Step 1"

    def test_store_output(self):
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
        executor.store_output(execution.execution_id, 0, "output data")
        output_path = Path(executor.outputs_dir) / execution.execution_id / "0.txt"
        assert output_path.exists()
