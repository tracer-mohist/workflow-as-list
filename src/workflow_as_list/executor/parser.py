# src/workflow_as_list/executor/parser.py
"""Workflow parser - converts workflow files into structured steps.

REFERENCE: docs/design/runtime/007-execution.md — Execution context design
"""

import re


class WorkflowParser:
    """Parse workflow files into structured steps.

    Supports 5 rules:
    1. content                   # List item
    2.  nested content           # Indent = sub-task (2 spaces)
    3. (tag) content             # Tag (can modify any line type)
    4. @tag[N]: condition?       # Jump (max N times)
    5. import: path              # Import other workflow

    Comment handling:
    - Lines starting with # are comments
    - Comments above a task line are attached to that task as metadata
    - File header comments are attached to the first task
    """

    def __init__(self, content: str):
        self.content = content
        self.lines = content.split("\n")
        self.steps: list[dict] = []
        self.tags: dict[str, int] = {}  # tag -> step index
        self.jumps: list[dict] = []  # jump definitions
        self.imports: list[str] = []

    def parse(self) -> list[dict]:
        """Parse workflow into steps.

        Comments above a task line are attached to that task as metadata.
        """
        pending_comments: list[str] = []

        for i, line in enumerate(self.lines):
            stripped = line.strip()

            # Skip empty lines
            if not stripped:
                continue

            # Collect comment lines
            if stripped.startswith("#"):
                pending_comments.append(stripped)
                continue

            # Parse task line (starts with -)
            if stripped.startswith("-"):
                step = self._parse_line(i, line, pending_comments)
                if step:
                    self.steps.append(step)
                    # Reset pending comments after attaching to task
                    pending_comments = []

        return self.steps

    def _parse_line(self, index: int, line: str, metadata: list[str]) -> dict | None:
        """Parse a single task line into a step."""
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        # Remove leading "- " from content
        content = stripped[1:].strip() if stripped.startswith("-") else stripped

        step = {
            "index": len(self.steps),
            "line_number": index + 1,
            "content": content,
            "indent": indent,
            "metadata": metadata.copy(),  # Attach pending comments
            "type": self._detect_type(content),
        }

        # Extract tag if present
        if content.startswith("("):
            match = re.match(r"\(([^)]+)\)\s*(.*)", content)
            if match:
                step["tag"] = match.group(1)
                step["content"] = match.group(2)
                self.tags[step["tag"]] = step["index"]

        # Extract jump if present
        if "@" in content:
            match = re.match(r"@(\w+)\[(\d+)\]:\s*(.*)", content)
            if match:
                step["jump_target"] = match.group(1)
                step["jump_limit"] = int(match.group(2))
                step["jump_condition"] = match.group(3)
                self.jumps.append(step)

        # Extract import if present
        if content.startswith("import:"):
            path = content.split("import:", 1)[1].strip()
            step["import_path"] = path
            self.imports.append(path)

        return step

    def _detect_type(self, content: str) -> str:
        """Detect line type."""
        if content.startswith("("):
            return "tagged"
        elif content.startswith("@"):
            return "jump"
        elif content.startswith("import:"):
            return "import"
        else:
            return "content"

    def validate_no_pure_import(self) -> tuple[bool, list[str]]:
        """Validate that workflow is not a pure-import file.

        Rules:
        1. File must have at least one non-import step
        2. Import cannot be the first non-comment line (ignition required)

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Check if file has any non-import steps
        non_import_steps = [s for s in self.steps if s["type"] != "import"]
        if not non_import_steps:
            errors.append(
                "Pure import file not allowed. "
                "Add local steps before or after import. "
                "Example: - (start) Workflow Name\\n    import: ./base.workflow.list"
            )
            return False, errors

        # Check if import is the first line (before any local step)
        first_step = self.steps[0] if self.steps else None
        if first_step and first_step["type"] == "import":
            errors.append(
                "Import cannot be the first line. "
                "Add ignition step before import. "
                "Example: - (start) Workflow Name\\n    import: ./base.workflow.list"
            )
            return False, errors

        return True, errors
