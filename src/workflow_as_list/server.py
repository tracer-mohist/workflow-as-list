# src/workflow_as_list/server.py
"""FastAPI HTTP server with OpenAPI support."""

from pathlib import Path

from fastapi import FastAPI, HTTPException

from .constants import ensure_directories
from .executor import Executor, WorkflowParser
from .models import AuditStatus


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title="WorkflowAsList API",
        description="HTTP API for workflow management",
        version="0.1.1",
    )

    # Initialize executor
    ensure_directories()
    executor = Executor()

    @app.get("/workflows", tags=["workflows"])
    def list_workflows():
        """List all registered workflows."""
        return executor.list_workflows()

    @app.get("/workflows/{name}", tags=["workflows"])
    def get_workflow(name: str):
        """Get workflow details."""
        workflow = executor.get_workflow(name)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return workflow

    @app.post("/workflows/{name}/approve", tags=["workflows"])
    def approve_workflow(name: str):
        """Approve workflow for execution."""
        workflow = executor.get_workflow(name)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        executor.update_workflow_status(name, AuditStatus.APPROVED)
        return {"status": "approved", "name": name}

    @app.post("/workflows/{name}/reject", tags=["workflows"])
    def reject_workflow(name: str):
        """Reject workflow."""
        workflow = executor.get_workflow(name)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        executor.update_workflow_status(name, AuditStatus.REJECTED)
        return {"status": "rejected", "name": name}

    @app.post("/workflows/{name}/run", tags=["executions"])
    def run_workflow(name: str):
        """Start workflow execution."""
        workflow = executor.get_workflow(name)
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")

        if workflow.status != AuditStatus.APPROVED:
            raise HTTPException(
                status_code=400,
                detail=f"Workflow not approved (status: {workflow.status.value})",
            )

        content = Path(workflow.file_path).read_text()
        parser = WorkflowParser(content)
        steps = parser.parse()

        execution = executor.create_execution(workflow, len(steps))
        return execution

    @app.get("/executions/{execution_id}", tags=["executions"])
    def get_execution(execution_id: str):
        """Get execution status."""
        execution = executor.get_execution(execution_id)
        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")
        return execution

    return app


# Create app instance for uvicorn
app = create_app()
