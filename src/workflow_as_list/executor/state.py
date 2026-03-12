# src/workflow_as_list/executor/state.py
"""Executor state management - workflow registry and execution tracking.

REFERENCE: docs/design/runtime/007-execution.md — Execution state files
REFERENCE: docs/design/overview/002-architecture.md — Executor role
"""

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

from ..models import AuditStatus, Execution, ExecutionStatus, Workflow


class Executor:
    """Execute workflows step-by-step.

    Features:
    - Progressive exposure (one step at a time)
    - Immutable flow during execution
    - State persistence to files
    """

    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.registry_path = config_dir / "registry.jsonl"
        self.executions_dir = config_dir / "executions"
        self.outputs_dir = config_dir / "outputs"

        # Ensure directories exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.executions_dir.mkdir(exist_ok=True)
        self.outputs_dir.mkdir(exist_ok=True)

    def register_workflow(
        self, name: str, file_path: Path, content: str, file_hash: str, token_count: int
    ) -> Workflow:
        """Register a workflow to registry.jsonl."""
        workflow = Workflow(
            name=name,
            hash=file_hash,
            file_path=str(file_path.absolute()),
            line_count=len(content.split("\n")),
            token_count=token_count,
        )

        # Append to registry (append-only)
        with open(self.registry_path, "a") as f:
            f.write(json.dumps(workflow.model_dump(mode="json")) + "\n")

        return workflow

    def get_workflow(self, name: str) -> Workflow | None:
        """Get latest workflow entry by name."""
        if not self.registry_path.exists():
            return None

        # Read registry (last entry wins)
        workflow = None
        with open(self.registry_path) as f:
            for line in f:
                entry = json.loads(line)
                if entry["name"] == name:
                    workflow = Workflow(**entry)

        return workflow

    def update_workflow_status(self, name: str, status: AuditStatus) -> bool:
        """Update workflow audit status."""
        if not self.registry_path.exists():
            return False

        # Read all entries
        entries = []
        with open(self.registry_path) as f:
            for line in f:
                entries.append(json.loads(line))

        # Update matching entry
        updated = False
        for entry in entries:
            if entry["name"] == name:
                entry["status"] = status.value
                entry["updated_at"] = datetime.now(UTC).isoformat()
                updated = True

        if not updated:
            return False

        # Rewrite registry
        with open(self.registry_path, "w") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")

        return True

    def create_execution(self, workflow: Workflow, steps_total: int) -> Execution:
        """Create a new execution instance."""
        execution_id = f"{workflow.name}-{uuid.uuid4().hex[:8]}"
        execution = Execution(
            execution_id=execution_id,
            workflow_name=workflow.name,
            workflow_hash=workflow.hash,
            steps_total=steps_total,
            outputs_path=str(self.outputs_dir / execution_id),
        )

        # Create outputs directory
        Path(execution.outputs_path).mkdir(exist_ok=True)

        # Save execution state
        self._save_execution(execution)

        return execution

    def _save_execution(self, execution: Execution) -> None:
        """Save execution state to file."""
        path = self.executions_dir / f"{execution.execution_id}.json"
        with open(path, "w") as f:
            json.dump(execution.model_dump(mode="json"), f, indent=2)

    def get_execution(self, execution_id: str) -> Execution | None:
        """Load execution from file."""
        path = self.executions_dir / f"{execution_id}.json"
        if not path.exists():
            return None

        with open(path) as f:
            data = json.load(f)
        return Execution(**data)

    def update_execution(self, execution: Execution) -> None:
        """Update execution state."""
        execution.updated_at = datetime.now(UTC)
        self._save_execution(execution)

    def get_next_step(self, execution: Execution, parser: object) -> dict | None:
        """Get next step for Agent (progressive exposure).

        Returns None if execution is complete.
        """
        if execution.current_step >= execution.steps_total:
            execution.status = ExecutionStatus.COMPLETED
            execution.completed_at = datetime.now(UTC)
            self.update_execution(execution)
            return None

        step = parser.steps[execution.current_step]
        return step

    def advance_execution(self, execution: Execution) -> Execution:
        """Advance to next step."""
        execution.current_step += 1
        execution.status = ExecutionStatus.RUNNING
        self.update_execution(execution)
        return execution

    def store_output(self, execution_id: str, step_index: int, output: str) -> None:
        """Store Agent output for a step."""
        output_path = Path(self.outputs_dir) / execution_id / f"{step_index}.txt"
        output_path.parent.mkdir(exist_ok=True)
        output_path.write_text(output)

    def list_workflows(self) -> list[Workflow]:
        """List all registered workflows."""
        if not self.registry_path.exists():
            return []

        workflows = []
        with open(self.registry_path) as f:
            for line in f:
                entry = json.loads(line)
                workflows.append(Workflow(**entry))

        return workflows
