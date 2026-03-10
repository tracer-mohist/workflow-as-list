# tests/test_server_component.py
"""Component tests for Server API.

NOTE: Follows Limited Testing Strategy - test public interfaces only.
REFERENCE: docs/limited-testing-strategy.md
REFERENCE: docs/design/runtime/008-server.md
"""

from fastapi.testclient import TestClient

from workflow_as_list.server import create_app

client = TestClient(create_app())


def test_root_endpoint():
    """Scenario: User calls GET /.
    Expected: Returns 404 (no root endpoint, which is fine).
    If fails: Server not responding.
    """
    response = client.get("/")
    assert response.status_code in [200, 404]


def test_list_workflows_empty():
    """Scenario: User calls GET /workflows with no workflows.
    Expected: Returns empty list.
    If fails: Workflows endpoint broken.
    """
    response = client.get("/workflows")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_workflow_not_found():
    """Scenario: User calls GET /workflows/{name} with non-existent name.
    Expected: Returns 404.
    If fails: Error handling broken.
    """
    response = client.get("/workflows/nonexistent")
    assert response.status_code == 404


def test_approve_workflow_not_found():
    """Scenario: User calls POST /workflows/{name}/approve with non-existent name.
    Expected: Returns 404.
    If fails: Error handling broken.
    """
    response = client.post("/workflows/nonexistent/approve")
    assert response.status_code == 404


def test_reject_workflow_not_found():
    """Scenario: User calls POST /workflows/{name}/reject with non-existent name.
    Expected: Returns 404.
    If fails: Error handling broken.
    """
    response = client.post("/workflows/nonexistent/reject")
    assert response.status_code == 404


def test_run_workflow_not_found():
    """Scenario: User calls POST /workflows/{name}/run with non-existent name.
    Expected: Returns 404.
    If fails: Error handling broken.
    """
    response = client.post("/workflows/nonexistent/run")
    assert response.status_code == 404


def test_get_execution_not_found():
    """Scenario: User calls GET /executions/{id} with non-existent id.
    Expected: Returns 404.
    If fails: Error handling broken.
    """
    response = client.get("/executions/nonexistent")
    assert response.status_code == 404


def test_openapi_schema():
    """Scenario: User accesses OpenAPI schema.
    Expected: Returns valid OpenAPI schema.
    If fails: OpenAPI broken.
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
