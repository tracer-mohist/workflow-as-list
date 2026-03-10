<!-- docs/design/runtime/007-execution.md -->
# Execution Context

Date: 2026-03-09
Status: Accepted
Authors: sha_dow, Tracer

---

## Purpose

Define execution instance and state management.

---

## Execution Instance

### Structure

Location: ~/.config/wf/executions/<name>-<timestamp>.json

```json
{
  "id": "deploy-20260309-184500",
  "workflow_name": "deploy-prod",
  "workflow_hash": "abc123...",
  "status": "RUNNING",
  "current_step": 3,
  "current_step_tag": "build",
  "steps_completed": [...],
  "started_at": "...",
  "updated_at": "..."
}
```

---

### Lifecycle

```
PENDING -> RUNNING -> COMPLETED
              |
              v
           FAILED
```

---

## State Persistence

### When to Persist

- After each step completes
- After status change
- Before exiting (graceful shutdown)

### Why Persist

- CLI is stateless
- Enable resume from interruption
- Audit trail

---

## Agent Focus Design

### Problem

Agent should not see multiple workflows concurrently.

---

### Solution

One execution instance active at a time.

Agent sees only current step of active execution.

---

### Implementation

Active execution:
- Loaded in memory
- Agent API calls use this context

Other executions:
- Persisted to files
- Not exposed to Agent

---

## Dependency Resolution

### Import Statement

```
import: ./common/setup.workflow.list
```

### Resolution

1. Parse import during workflow parsing
2. Find dependency in registry.jsonl
3. Check status:
   - APPROVED: Load content
   - Other: Error "dependency requires audit"
4. Cache dependency content
5. Continue execution

---

## Output Storage

Location: ~/.config/wf/outputs/<execution-id>/<step>.txt

Why separate files:
- Output may be large
- Keep state JSON small
- Enable streaming

---

## Queue Design

### Implicit Queue

No explicit queue management commands.

When workflow run called:
- No active execution: Start immediately
- Active execution: Queue automatically

---

### View Queue

```
workflow list

Shows:
- RUNNING: Currently executing
- QUEUED: Waiting
- Other: Not in queue
```

---

## Design Decisions

DECISION: 2026-03-09 — One active execution at a time.

WHY: Agent focus. Context isolation.

---

DECISION: 2026-03-09 — Implicit queue.

WHY: Simplicity. Most users don't need complex control.

---

DECISION: 2026-03-09 — Output in separate files.

WHY: Keep state JSON small. Enable streaming.

---

## Related Documents

REFERENCE: ../overview/002-architecture.md — Architecture overview
REFERENCE: ../cli/003-commands.md — CLI commands

---

Last Updated: 2026-03-09
