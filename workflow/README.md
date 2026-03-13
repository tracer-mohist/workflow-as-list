# Self-Hosted Workflows

Purpose: Use workflow-as-list to develop workflow-as-list.

Philosophy: If we want others to trust our rules, we must use them ourselves.

---

## What

Workflows in this directory manage our own development.

Not generic templates — project-specific.

---

## Why

1. **Validation** — Real usage exposes abstraction leaks
2. **Feedback** — Fast iteration (use → find issues → improve)
3. **Trust** — We eat our own dogfood

---

## Usage

```bash
uv run workflow check workflow/<name>.workflow.list
uv run workflow approve <name>
uv run workflow run <name>
```

---

## Relationship with examples/

| `workflow/` | `examples/` |
|-------------|-------------|
| We use | Others learn |
| Project-specific | General templates |
| Evolves fast | Stable |

---

See: `examples/README.md` (design philosophy)
