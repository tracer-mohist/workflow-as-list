<!-- docs/design/overview/001-principles.md -->
# Design Principles

Date: 2026-03-09
Status: Accepted
Authors: sha_dow, Tracer

---

## Purpose

Core design philosophy for WorkflowAsList.

---

## Core Philosophy

WorkflowAsList is for production work, not casual chat.

Design decisions prioritize:
- Clarity over convenience
- Safety over flexibility
- Discipline over freedom

---

## UNIX Philosophy

### Minimal Complete Set

Each module does one thing well.

7 CLI subcommands. 6 API endpoints. No more.

### Independence

Each module works independently.

CLI works without server. Server shares CLI logic.

### Simple Configuration

INI format. Optional. Sensible defaults.

---

## Security Philosophy

### Explicit Over Implicit

Nothing hidden. Everything declared.

Whitelist empty by default. User configures intentionally.

### Transparency Over Obscurity

Security through verification, not hiding.

All content visible. All actions logged.

### Defense In Depth

7 security layers. Each layer independent.

Layer failure does not compromise system.

---

## Execution Philosophy

### Progressive Exposure

Executor exposes one step at a time to Agent.

Agent never sees full workflow.

### Immutable Flow

Execution flow cannot be modified during run.

No skip. No retry. No jump override.

### State Persistence

All state persisted to files.

CLI is stateless. Files enable resume.

---

## Output Philosophy

### Agent-Readable

Output is part of Agent prompt.

Design for: Readability, Comprehensibility, Maintainability.

### Prefix Identification

[TYPE] prefix for quick recognition.

Agent identifies output type in 1 token.

### Next Step Guidance

Every output ends with action guidance.

Agent always knows what to do next.

---

## Documentation Philosophy

### Lists Over Tables

Linear attention flow (~1.37 bits entropy).

Tables are 2D (~2.32 bits entropy).

### ASCII Only

Maximum encoding compatibility.

No emoji. No special Unicode.

### Annotation

LABEL: content format.

NOTE, REFERENCE, TIP, DECISION.

---

## Design Decisions

DECISION: 2026-03-09 — 7 CLI subcommands only.

WHY: Minimal complete set. UNIX philosophy.

---

DECISION: 2026-03-09 — Execution immutable.

WHY: Audit trail integrity. No skip/retry.

---

DECISION: 2026-03-09 — Output uses [TYPE] prefix.

WHY: Agent identifies type in 1 token.

---

## Related Documents

REFERENCE: ../cli/003-commands.md — CLI commands
REFERENCE: ../security/005-layers.md — Security layers
REFERENCE: ../../research/cognitive/001-hiding.md — Cognitive hiding theory

---

Last Updated: 2026-03-09
