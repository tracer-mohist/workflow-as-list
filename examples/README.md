# Examples

Purpose: Reusable workflow templates.

Not here: Project-specific workflows → `workflow/`

---

## Naming

Format: `<path>/<action>.workflow.list`

- `<path>`: Directory path (any depth, at least 1 level)
- `<action>`: Single segment (workflow name, no slashes)

Rule: Last segment before `.workflow.list` is the action.

Examples:
- `git/commit.workflow.list` → action=`commit`
- `github/issue/create.workflow.list` → action=`create`
- `general/code/review.workflow.list` → action=`review`

---

## Constraints

1. **General** — No project-specific assumptions
2. **Stable** — Templates should not change often
3. **Documented** — Comments explain WHY, not just WHAT

---

## Usage

```bash
workflow check examples/<path>
workflow run examples/<path>
```

Query structure: `ls -R examples/`

---

## Self-Hosting

Templates are extracted from `workflow/` (our own usage).

See: `workflow/README.md`

---

Last Updated: 2026-03-13
