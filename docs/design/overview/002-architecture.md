<!-- docs/design/overview/002-architecture.md -->
# Architecture Overview

Date: 2026-03-09
Status: Accepted
Authors: sha_dow, Tracer

---

## Purpose

High-level architecture overview.

---

## Core Components

```
User
  |
  v
CLI (workflow command)
  |
  v
Executor (interpreter)
  |
  v
Agent (LLM API)
```

---

## Executor Role

Executor is interpreter, not direct executor.

Responsibilities:
- Parse workflow syntax
- Validate encoding and syntax
- Check blacklist
- Manage execution state
- Expose one step at a time to Agent
- Evaluate jump conditions

---

## Execution Phases

### Phase 1: Registration

```
workflow check <file>
  |
  v
Validate (encoding, syntax, tokens, blacklist)
  |
  v
Register to registry.jsonl
  |
  v
Status: PENDING_AUDIT
```

---

### Phase 2: Audit

```
workflow approve <name>
  |
  v
Human review features
  |
  v
Append approval to registry.jsonl
  |
  v
Status: APPROVED
```

---

### Phase 3: Execution

```
workflow run <name>
  |
  v
Verify APPROVED + hash match
  |
  v
Create execution instance
  |
  v
Execute loop (one step at a time)
  |
  v
Status: COMPLETED
```

---

## State Files

### registry.jsonl

Location: ~/.config/wf/registry.jsonl

Purpose: Track all workflows, hashes, audit status.

Format: JSONL (append-only).

---

### Execution Instances

Location: ~/.config/wf/executions/<name>-<timestamp>.json

Purpose: Track execution progress.

---

### Output Files

Location: ~/.config/wf/outputs/<execution-id>/<step>.txt

Purpose: Store Agent output per step.

---

## CLI and Server

### Shared Logic

CLI and Server share:
- Executor implementation
- Security checks
- State files

Why: Consistency. Single source of truth.

---

### CLI Mode

Short-lived. Command-based.

Stateless (state in files).

---

### Server Mode

Long-running. HTTP API.

Binds to 127.0.0.1:8080 by default.

---

## Design Decisions

DECISION: 2026-03-09 — Executor is interpreter.

WHY: Progressive exposure enables audit and control.

---

DECISION: 2026-03-09 — CLI and Server share state.

WHY: Consistency. Single source of truth.

---

## Related Documents

REFERENCE: ../cli/003-commands.md — CLI commands
REFERENCE: ../runtime/007-execution.md — Execution details
REFERENCE: ../security/005-layers.md — Security layers

---

Last Updated: 2026-03-09
