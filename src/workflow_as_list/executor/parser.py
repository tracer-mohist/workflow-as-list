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
    """

    def __init__(self, content: str):
        self.content = content
        self.lines = content.split("\n")
        self.steps: list[dict] = []
        self.tags: dict[str, int] = {}  # tag -> step index
        self.jumps: list[dict] = []  # jump definitions
        self.imports: list[str] = []

    def parse(self) -> list[dict]:
        """Parse workflow into steps."""
        for i, line in enumerate(self.lines):
            if not line.strip():
                continue

            step = self._parse_line(i, line)
            if step:
                self.steps.append(step)

        return self.steps

    def _parse_line(self, index: int, line: str) -> dict | None:
        """Parse a single line into a step."""
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        step = {
            "index": len(self.steps),
            "line_number": index + 1,
            "content": stripped,
            "indent": indent,
            "type": self._detect_type(stripped),
        }

        # Extract tag if present
        if stripped.startswith("("):
            match = re.match(r"\(([^)]+)\)\s*(.*)", stripped)
            if match:
                step["tag"] = match.group(1)
                step["content"] = match.group(2)
                self.tags[step["tag"]] = step["index"]

        # Extract jump if present
        if "@" in stripped:
            match = re.match(r"@(\w+)\[(\d+)\]:\s*(.*)", stripped)
            if match:
                step["jump_target"] = match.group(1)
                step["jump_limit"] = int(match.group(2))
                step["jump_condition"] = match.group(3)
                self.jumps.append(step)

        # Extract import if present
        if stripped.startswith("import:"):
            path = stripped.split("import:", 1)[1].strip()
            step["import_path"] = path
            self.imports.append(path)

        return step

    def _detect_type(self, line: str) -> str:
        """Detect line type."""
        if line.startswith("("):
            return "tagged"
        elif line.startswith("@"):
            return "jump"
        elif line.startswith("import:"):
            return "import"
        elif line.startswith(" "):
            return "nested"
        else:
            return "content"
