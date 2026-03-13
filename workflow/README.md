# Self-Hosted Workflows

Purpose: Use workflow-as-list to develop workflow-as-list.

Not here: Generic templates → `examples/`

---

## Mapping

Format: `workflow/<name>.workflow.list`

- `<name>`: Workflow identifier (single segment)

Rule: Flat structure, routed by `main.workflow.list` (TODO).

---

## Constraints

1. **Project-Specific** — Binds to workflow-as-list
2. **Evolving** — Changes with project needs
3. **Validated** — Must be used in real work

---

## Usage

```bash
workflow check workflow/<name>
workflow approve <name>
workflow run <name>
```

Query structure: `ls workflow/`

---

## Philosophy

If we want others to trust our rules, we must use them ourselves.

See: `examples/README.md` (template extraction)

---

Last Updated: 2026-03-13
