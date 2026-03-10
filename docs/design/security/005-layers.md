<!-- docs/design/security/005-layers.md -->
# Security Layers

Date: 2026-03-09
Status: Accepted
Authors: sha_dow, Tracer

---

## Purpose

Define 7 security layers.

---

## Core Philosophy

Explicit over implicit. Transparency over obscurity.

---

## Layer 1: Encoding Check

Check: Printable ASCII only (0x20-0x7E)

Why: No homoglyph attacks, no hidden characters.

REFERENCE: ../../../research/encoding/002-ascii.md

---

## Layer 2: Blacklist Check

Check: Substring match against keywords

When: Check phase + Run phase (double check)

Effect: Absolute rejection (cannot override)

Examples: rm -rf, eval(, exec(, /etc/passwd

---

## Layer 3: Syntax Validation

Check: workflow-as-list DSL 5 rules

Why: Ensure well-formed structure.

---

## Layer 4: Token Length Check

Check: Each step 282-358 bytes (approximate tokens)

Formula: sqrt(N * 0.618) to sqrt(N)

Why: Prevent context injection and cognitive overload.

REFERENCE: ../../../research/theory/003-limits.md

---

## Layer 5: Feature Scan

Scan for: Base64, URL, IP address, command keywords

Output: audit-checklist.json

Why: Alert human reviewer.

---

## Layer 6: Human Audit

Requirement: Human must approve before execution.

Agent role: Review features, notify human of risks.

---

## Layer 7: Whitelist Check

When: Audit phase (optional, empty by default)

Types: Network whitelist, Command whitelist

Effect: Required for execution if configured.

NOTE: Whitelist is opt-in. Default empty.

---

## Audit Flow

```
workflow check <file>
  |
  v
Layers 1-4 (automated)
  |
  v
Status: PENDING_AUDIT
  |
  v
Layer 5 (feature scan)
  |
  v
Layer 6 (human review)
  |
  v
Status: APPROVED or REJECTED
```

---

## Pre-Execution Checks

Before execution:
1. Status must be APPROVED
2. Hash must match approved hash
3. Blacklist re-check (execution time)
4. Import dependencies must be APPROVED

---

## Threat Model

| Attack | Defense |
|--------|---------|
| Prompt injection | Token limits |
| Command injection | Blacklist + whitelist |
| Data exfiltration | Network whitelist |
| Supply chain (import) | Dependency audit chain |
| File traversal | Path validation, hash binding |

---

## Design Decisions

DECISION: 2026-03-09 — Blacklist checked twice.

WHY: Defense in depth.

---

DECISION: 2026-03-09 — Whitelist is opt-in.

WHY: Explicit over implicit.

---

DECISION: 2026-03-09 — Blacklist is absolute.

WHY: Some patterns always dangerous.

---

## Related Documents

REFERENCE: 006-config.md — Configuration format
REFERENCE: ../overview/001-principles.md — Security philosophy
REFERENCE: ../../../research/encoding/002-ascii.md — Encoding theory

---

Last Updated: 2026-03-09
