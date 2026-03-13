<!-- README.md -->
# WorkflowAsList

Workflows are Just Lists.

NOTE: Language is WorkflowAsList DSL (file extension: `.workflow.list`)

A thinking constraint DSL for structuring LLM interactions.

---

## Purpose

Filter noise, focus thinking, prevent divergence.

NOTE: This DSL is for thinking constraint, not for execution.

---

## Quick Start

### Install

Users (pipx):
```bash
pipx install git+https://github.com/tracer-mohist/workflow-as-list.git
```

Contributors (uv):
```bash
git clone https://github.com/tracer-mohist/workflow-as-list.git
cd workflow-as-list
uv sync
```

### Explore

CLI:
```bash
workflow --help        # All commands
workflow <cmd> --help  # Command details
```

Server API:
```
http://localhost:8080/docs     # OpenAPI UI
http://localhost:8080/openapi.json  # OpenAPI schema
```

### Write

See `SYNTAX.md` for DSL syntax.
See `examples/` for example workflows.

---

## Core Concept

### Progressive Reading

workflow-as-list is a reader, not an executor.

Like reading a book:
1. Read current step
2. Understand and execute
3. Advance to next step
4. Cannot skip unread steps

Agent workflow:
```
workflow run <name>           # Create execution
workflow exec read <id>       # Read step (mark as read)
[Agent executes operations]   # Using own tools
workflow exec next <id>       # Advance (must read first)
```

---

## State Management

Default location: `~/.workflow-as-list/`

- `config.ini` — Configuration
- `registry.jsonl` — Registered workflows
- `state/executions/` — Execution instances
- `state/outputs/` — Step outputs

Reset all state:
```bash
rm -rf ~/.workflow-as-list/
```

---

## Documentation

- Syntax: `SYNTAX.md`, `SYNTAX.ebnf`
- Design: `docs/design/`
- Contributing: `CONTRIBUTING.md`
- Commit convention: `.github/COMMIT_CONVENTION.md`

---

Author: Tracer (Chinese: 迹，Ji)
Created: 2026-03-08
Last Updated: 2026-03-13
