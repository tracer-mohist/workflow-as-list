<!-- docs/design/cli/003-commands.md -->
# CLI Commands

Date: 2026-03-09
Status: Accepted
Authors: sha_dow, Tracer

---

## Purpose

Define CLI subcommands and usage.

---

## Command Name

workflow

Why: Full name, readable, tab-completion.

---

## Core Subcommands (7)

### Registration

**workflow check <file>**

Purpose: Syntax check, blacklist check, token check, register.

Output: PENDING_AUDIT status.

---

### Audit

**workflow approve <name>**

Purpose: Approve workflow for execution.

**workflow reject <name>**

Purpose: Reject workflow.

---

### Execution

**workflow run <name>**

Purpose: Execute approved workflow.

Requirement: Status = APPROVED, hash matches.

---

### Query

**workflow list**

Purpose: List all workflows with status.

**workflow show <name>**

Purpose: Show workflow details and logs.

---

### Server

**workflow serve**

Purpose: Start HTTP server.

Options: --host, --port

---

### Help

**workflow help [command]**

Purpose: Show help information.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Configuration error |
| 3 | Syntax/blacklist error |
| 4 | Audit not passed |
| 5 | Hash mismatch |
| 6 | File not found |
| 7 | Permission denied |
| 8 | Network error |
| 9 | Server error |

---

## Configuration

### Location

Global: ~/.config/wf/config.ini

Project: .wf/config.ini (optional, future)

---

### Loading

1. Load global config (if exists)
2. Load project config (if exists)
3. Use defaults for missing values

---

## Design Decisions

DECISION: 2026-03-09 — 7 core subcommands only.

WHY: Minimal complete set. UNIX philosophy.

---

DECISION: 2026-03-09 — No step skip/retry commands.

WHY: Execution flow immutable. Audit trail integrity.

---

## Related Documents

REFERENCE: 004-output.md — Output format
REFERENCE: ../overview/001-principles.md — Design principles
REFERENCE: ../security/005-layers.md — Security checks

---

Last Updated: 2026-03-09
