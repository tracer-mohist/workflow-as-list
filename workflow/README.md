# WorkflowAsList Self-Hosted Workflows

Purpose: Manage workflow-as-list project development using workflow-as-list.

Not here: Generic templates → `examples/` (for others to learn)

---

## What Is This?

This directory contains workflows that we use to develop workflow-as-list itself.

Philosophy: If we want others to trust our DSL, we must use it ourselves.

---

## Why Self-Hosting?

### 1. Validation

Real usage exposes abstraction leaks.

If workflow-as-list cannot manage its own development, why should others use it?

### 2. Feedback Loop

```
Use workflow → Find issues → Improve DSL → Use again
```

This is the fastest iteration path.

### 3. Trust

"We use it ourselves" is more powerful than any marketing.

This is honest practice.

---

## Directory Structure

```
workflow/
├── README.md              # This file (purpose and usage)
├── commit.workflow.list   # Commit guide (project-specific rules)
├── main.workflow.list     # Daily development entry point (TODO)
├── push.workflow.list     # Push + CI check (TODO)
└── release.workflow.list  # Release process (TODO)
```

---

## Usage

### Run a workflow

```bash
uv run workflow check workflow/<name>.workflow.list
uv run workflow approve <name>.workflow
uv run workflow run <name>.workflow
```

### Add a new workflow

1. Create `workflow/<name>.workflow.list`
2. Test with `uv run workflow check workflow/<name>.workflow.list`
3. Use it in real work
4. Iterate based on experience

---

## Workflow Naming

Format: `<action>.workflow.list`

Examples:
- `commit.workflow.list` — Commit message guide
- `push.workflow.list` — Push with CI check
- `release.workflow.list` — Release process

Why flat structure:
- Single entry point (`main.workflow.list`) routes to sub-workflows
- Avoids deep nesting for project-specific workflows
- Clear separation from `examples/` (which uses `<domain>/<action>/`)

---

## Design Principles

### 1. Project-Specific

These workflows are绑定 to workflow-as-list project.

They contain:
- Project-specific rules (directory → commit type mapping)
- Custom validation (sensitive file checks)
- Team conventions (review process)

Do NOT copy directly to other projects without adaptation.

### 2. Evolving Fast

Unlike `examples/` (stable templates), `workflow/` evolves with the project.

Expect frequent updates as we:
- Discover better patterns
- Fix pain points
- Add new operations

### 3. Progressive Design

Workflow design process:

Phase 1: Record — Document successful operations
Phase 2: Abstract — Extract common patterns
Phase 3: Formalize — Write as `.workflow.list`
Phase 4: Validate — Use it, find issues, iterate

---

## Relationship with examples/

| Aspect | `workflow/` | `examples/` |
|--------|-------------|-------------|
| Purpose | Self-hosted (we use) | Templates (others learn) |
| Stability | Evolves fast | Stable |
| Specificity | Project-specific | General |
| Audience | Project developers | External users |

Flow:
```
workflow/ (real usage)
  ↓ Extract patterns
examples/ (generalized templates)
```

---

## Current Workflows

### commit.workflow.list

Purpose: Guide Conventional Commits for workflow-as-list.

Features:
- Directory → type mapping (src/→feat, tests/→test, etc.)
- Sensitive file validation
- Body/footer guidance

Usage:
```bash
uv run workflow run commit.workflow
```

---

## TODO

Workflows to add:

- `main.workflow.list` — Daily entry point (routes to sub-workflows)
- `push.workflow.list` — Push with CI status check
- `release.workflow.list` — Release process (version bump, tag, publish)
- `issue/` — Issue triage and response
- `pr/` — PR review and merge

---

## Related Files

- `examples/README.md` — Generic template design philosophy
- `.github/COMMIT_CONVENTION.md` — Commit message rules
- `docs/AGENT-INTEGRATION.md` — How agents use workflows

---

Last Updated: 2026-03-13 (self-hosting bootstrap)
