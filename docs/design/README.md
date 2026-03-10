<!-- docs/design/README.md -->
# Design Index

Purpose: Finalized specifications and architecture decisions.

Status: Documents here are committed design decisions.

---

## Reading Order

For implementers:
1. overview/001-principles.md — Design philosophy
2. overview/002-architecture.md — Architecture overview
3. cli/003-commands.md — CLI commands
4. cli/004-output.md — Output format
5. security/005-layers.md — Security layers
6. security/006-config.md — Configuration
7. runtime/007-execution.md — Execution context
8. runtime/008-server.md — Server design

---

## Documents by Category

### Overview

**overview/001-principles.md**

Purpose: Core design philosophy.

Key concepts:
- UNIX philosophy (minimal, independent)
- Security philosophy (explicit, transparent)
- Execution philosophy (progressive exposure, immutable)
- Output philosophy (Agent-readable)

---

**overview/002-architecture.md**

Purpose: High-level architecture overview.

Key concepts:
- Executor role (interpreter, not direct executor)
- Execution phases (Registration, Audit, Execution)
- State files (registry.jsonl, executions, outputs)
- CLI and Server relationship

---

### CLI

**cli/003-commands.md**

Purpose: CLI subcommands and usage.

Key concepts:
- 7 core subcommands (check, approve, reject, run, list, show, serve)
- Exit codes
- Configuration loading

---

**cli/004-output.md**

Purpose: Output format for CLI.

Key concepts:
- [TYPE] prefix
- Lists, not tables
- Next step guidance
- Templates and examples

---

### Security

**security/005-layers.md**

Purpose: 7 security layers.

Key concepts:
- Encoding check (ASCII only)
- Blacklist check (substring match)
- Token length check (282-358 bytes)
- Feature scan
- Human audit
- Whitelist check (opt-in)

---

**security/006-config.md**

Purpose: Configuration format.

Key concepts:
- INI format
- Blacklist/whitelist format
- Loading order
- Defaults

---

### Runtime

**runtime/007-execution.md**

Purpose: Execution context and state management.

Key concepts:
- Execution instance structure
- Lifecycle (PENDING → RUNNING → COMPLETED)
- Agent focus design
- Dependency resolution
- Implicit queue

---

**runtime/008-server.md**

Purpose: HTTP server and REST API.

Key concepts:
- 6 API endpoints
- Shared state with CLI
- Authentication (optional)
- WebSocket (future)

---

## Design Principles

### UNIX Philosophy

- Minimal complete set
- Each module works independently
- Simple configuration (INI)

---

### Security

- Explicit over implicit
- Transparency over obscurity
- Defense in depth (7 layers)

---

### Output

- Readability (Agent understands quickly)
- Comprehensibility (no ambiguity)
- Maintainability (easy to update)

---

## Related Indexes

- Research documents: see: ../research/README.md
- Project overview: see: ../../README.md
- Syntax specification: see: ../../SYNTAX.md

---

Status: Active design documentation
Last Updated: 2026-03-09
