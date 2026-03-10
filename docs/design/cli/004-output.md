<!-- docs/design/cli/004-output.md -->
# Output Format

Date: 2026-03-09
Status: Accepted
Authors: sha_dow, Tracer

---

## Purpose

Define output format for CLI. Optimized for Agent readability.

---

## Core Principle

Output is part of Agent prompt.

Design for: Readability, Comprehensibility, Maintainability.

---

## Format Rules

### Encoding

ASCII only. No emoji. No special Unicode.

---

### Structure

Lists, not tables.

Why: Linear attention flow.

---

### Prefix

[TYPE] prefix for quick identification.

Examples:
- [CHECK] — Check result
- [APPROVE] — Audit approval
- [RUN] — Execution status
- [LIST] — Workflow list
- [SHOW] — Workflow details
- [ERROR] — Error message

---

### Core Info First

First line: One sentence summary.

---

### Details as Lists

```
Details:
- Field 1: Value
- Field 2: Value
```

---

### Next Step

End with action guidance.

Example: Next: workflow approve deploy-prod

---

## Templates

### Success

```
[TYPE] Name - Status

Core info (1 sentence).

Details:
- Field 1: Value
- Field 2: Value

Next: Action guidance
```

---

### Error

```
[ERROR] Error type

Problem description.

Reason:
- Reason 1
- Reason 2

Resolution:
1. Step 1
2. Step 2

Security note: (if applicable)
```

---

## Examples

### Check

```
[CHECK] deploy-prod.workflow.list

Syntax check passed.

Details:
- Encoding: ASCII only OK
- Syntax: valid DSL OK
- Token length: 282-358 bytes/step OK
- Blacklist: no match OK

Features detected:
- URL: line 12, "https://github.com"
- Command: line 15, "git push"

Status: PENDING_AUDIT
Next: workflow approve deploy-prod
```

---

### List

```
[LIST] Workflows

Name                Status              Step        Updated
--------------------------------------------------------------------------------
deploy-prod         RUNNING             step-3      2m ago
test-suite          QUEUED              -           5m ago
cleanup             PENDING_AUDIT       -           1h ago

Stats:
- Total: 3
- Running: 1
- Queued: 1
- Pending audit: 1

Next: workflow show <name> (view details)
```

NOTE: Space-aligned, not table syntax.

---

### Error

```
[ERROR] Workflow not approved

Name: deploy-prod
Status: PENDING_AUDIT

Reason:
This workflow has not been audited.

Resolution:
1. Review: workflow show deploy-prod
2. Approve: workflow approve deploy-prod
3. Execute: workflow run deploy-prod

Security note: Do not skip audit steps.
```

---

## Time Format

Absolute: 2026-03-09T18:45:00Z (logs, timestamps)

Relative: 2m ago, 1h ago (list output)

---

## Path Format

Use tilde: ~/.config/wf/outputs/...

Not full: /home/user/.config/wf/outputs/...

---

## Design Decisions

DECISION: 2026-03-09 — Output uses [TYPE] prefix.

WHY: Agent identifies type in 1 token.

---

DECISION: 2026-03-09 — Lists, not tables.

WHY: Linear attention flow. Lower entropy.

---

DECISION: 2026-03-09 — Every output ends with Next step.

WHY: Clear action guidance.

---

## Related Documents

REFERENCE: 003-commands.md — CLI commands
REFERENCE: ../../../.openclaw/workspace/docs/prompt-engineering/README.md

---

Last Updated: 2026-03-09
