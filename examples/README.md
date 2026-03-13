# Examples - WorkflowAsList DSL Examples

Purpose: Demonstrate DSL patterns and provide reusable templates.

Not here: Project-specific workflows → `workflow/` (self-hosted)

---

## Design Philosophy

### 1. Naming Convention

Format: `<domain>/<action>.workflow.list`

Examples:
- `github/issue/create.workflow.list` — Create GitHub issue
- `git/commit.workflow.list` — Conventional Commits
- `general/code/review.workflow.list` — Code review process

Why:
- Directory as namespace (clear semantics)
- Verb-first for actions (intent clarity)
- Scalable nesting (sub-domains natural)

REFERENCE: memory/2026-03-13.md (naming discussion)

---

### 2. Layer Separation

Three layers:

Layer 0: CLI/Server (executor)
  ↓
Layer 1: `workflow/*.workflow.list` (self-hosted, project-specific)
  ↓
Layer 2: `examples/*.workflow.list` (general templates, for others)

Why:
- Examples are stable (reference templates)
- Workflow/ evolves fast (real usage)
- Prevents mixing concerns

---

### 3. Bootstrap Principle

From memory/2026-03-13.md:

> If we want others to trust our rules, we must use them ourselves.

Self-hosting strategy:
1. Use workflow-as-list to develop workflow-as-list
2. Extract patterns from `workflow/` to `examples/`
3. Validate DSL expressiveness in real scenarios

Why:
- Trust comes from usage, not design
- Real scenarios expose abstraction leaks
- Honest practice (we eat our own dogfood)

---

### 4. Progressive Design

Workflow design process:

Phase 1: Record — Document successful operations
Phase 2: Abstract — Extract common patterns
Phase 3: Formalize — Write as `.workflow.list`
Phase 4: Validate — Use it, find issues, iterate

Why:
- Workflows grow from practice, not speculation
- Allows failure (discard bad designs)
- Emergent complexity (simple rules → rich behavior)

---

## Directory Structure

```
examples/
├── git/                     # Git operations (universal)
│   └── commit.workflow.list    # Conventional Commits guide
│
├── github/                  # GitHub operations
│   └── issue/
│       ├── create.workflow.list
│       └── close.workflow.list
│
├── general/                 # Cross-platform workflows
│   └── code/
│       ├── review.workflow.list
│       └── format.workflow.list
│
└── README.md                # This file (design philosophy)
```

---

## Usage

### Run an example

```bash
workflow check examples/git/commit.workflow.list
workflow run examples/git/commit.workflow.list
```

### Adapt for your project

1. Copy to your project
2. Modify domain-specific rules
3. Test and iterate

---

## Contributing

When adding new examples:

1. Follow naming convention (`<domain>/<action>.workflow.list`)
2. Keep it general (avoid project-specific assumptions)
3. Add comments explaining WHY (not just WHAT)
4. Test with `workflow check <file>`

---

## Related Files

- `workflow/` — Self-hosted workflows (project-specific)
- `docs/` — DSL concepts and principles
- `SYNTAX.md` — Language specification

---

Last Updated: 2026-03-13 (bootstrap design discussion)
