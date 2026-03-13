# tests/test_parser.py
"""Unit tests for workflow parser.

Tests comment attachment to tasks.
"""

from workflow_as_list.executor.parser import WorkflowParser


class TestCommentAttachment:
    """Test that comments are attached to tasks as metadata."""

    def test_file_header_comments_attach_to_first_task(self):
        """Scenario: File has header comments before first task.
        Expected: First task has all header comments in metadata.
        """
        content = """# Workflow: Test
# Purpose: Testing

- (start) First task
"""
        parser = WorkflowParser(content)
        steps = parser.parse()

        assert len(steps) == 1
        assert len(steps[0]["metadata"]) == 2
        assert "# Workflow: Test" in steps[0]["metadata"]
        assert "# Purpose: Testing" in steps[0]["metadata"]

    def test_comments_between_tasks_attach_to_next_task(self):
        """Scenario: Comments between two tasks.
        Expected: Comments attach to second task, not first.
        """
        content = """- (start) First task

# WHY: Important context
- (compose) Second task
"""
        parser = WorkflowParser(content)
        steps = parser.parse()

        assert len(steps) == 2
        assert len(steps[0]["metadata"]) == 0  # First task has no comments
        assert len(steps[1]["metadata"]) == 1  # Second task has comment
        assert "# WHY: Important context" in steps[1]["metadata"]

    def test_nested_comments_attach_to_nested_task(self):
        """Scenario: Comments before nested task.
        Expected: Comments attach to nested task.
        """
        content = """- (start) Parent task
  # NOTE: Child context
  - Child task
"""
        parser = WorkflowParser(content)
        steps = parser.parse()

        assert len(steps) == 2
        assert steps[1]["metadata"] == ["# NOTE: Child context"]

    def test_empty_metadata_when_no_comments(self):
        """Scenario: Task has no comments above it.
        Expected: Empty metadata list.
        """
        content = """- (start) Task without comments
"""
        parser = WorkflowParser(content)
        steps = parser.parse()

        assert len(steps) == 1
        assert steps[0]["metadata"] == []

    def test_comment_format_preserved(self):
        """Scenario: Comments have various formats.
        Expected: Full comment line preserved (including #).
        """
        content = """# =============================================================================
# Header
# =============================================================================
#
# Blank line in comments
#
- (start) Task
"""
        parser = WorkflowParser(content)
        steps = parser.parse()

        assert len(steps[0]["metadata"]) == 6
        assert (
            "# ============================================================================="
            in steps[0]["metadata"]
        )
        assert "#" in steps[0]["metadata"]  # Blank comment line
