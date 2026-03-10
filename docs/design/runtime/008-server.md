<!-- docs/design/runtime/008-server.md -->
# Server Design

Date: 2026-03-09
Status: Accepted
Authors: sha_dow, Tracer

---

## Purpose

Define HTTP server and REST API.

---

## Core Concept

Server is HTTP wrapper around CLI logic.

CLI and Server share same Executor, same state files.

---

## Architecture

```
workflow serve

1. Load configuration
2. Bind to host:port (default: 127.0.0.1:8080)
3. Register routes (OpenAPI endpoints)
4. Enter event loop
5. Handle requests asynchronously
6. Graceful shutdown on signal
```

---

## REST API Endpoints

### Base Path

/api/v1

---

### Core Endpoints

| Method | Endpoint | CLI Equivalent |
|--------|----------|----------------|
| POST | /workflows | workflow check |
| POST | /workflows/{name}/run | workflow run |
| POST | /workflows/{name}/approve | workflow approve |
| GET | /workflows | workflow list |
| GET | /workflows/{name} | workflow show |
| GET | /health | (health check) |

---

## Request/Response

### Content-Type

Application/json (all endpoints)

Exception: POST /workflows (multipart for file)

---

### Success Response

```json
{
  "status": "success",
  "data": {...}
}
```

---

### Error Response

```json
{
  "status": "error",
  "code": "WORKFLOW_NOT_APPROVED",
  "message": "Workflow not audited.",
  "resolution": "POST /workflows/{name}/approve"
}
```

---

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request |
| 403 | Forbidden |
| 404 | Not found |
| 409 | Conflict |
| 500 | Server error |

---

## State Management

### Shared State

Server and CLI share:
- registry.jsonl
- executions/*.json
- outputs/*/*.txt

Why: Consistency. Single source of truth.

---

### Concurrency

Server handles multiple requests concurrently.

State files use append-only semantics.

No locking required for reads.

---

## Authentication

### Default: None

Server binds to 127.0.0.1 by default.

Local network is trusted.

---

### Optional: API Key

Config:
```ini
[server]
enable_auth = true
api_key = <secret>
```

Header: X-API-Key: <secret>

---

## WebSocket (Optional)

Endpoint: WS /api/v1/executions/{id}/stream

Purpose: Push execution progress.

NOTE: Future enhancement.

---

## Design Decisions

DECISION: 2026-03-09 — Server shares state with CLI.

WHY: Consistency. Single source of truth.

---

DECISION: 2026-03-09 — Default bind to 127.0.0.1.

WHY: Security. Local only unless configured.

---

DECISION: 2026-03-09 — Authentication optional.

WHY: Simplicity. Most users run locally.

---

## Related Documents

REFERENCE: ../overview/002-architecture.md — Architecture
REFERENCE: ../cli/003-commands.md — CLI commands
REFERENCE: ../security/005-layers.md — Security

---

Last Updated: 2026-03-09
