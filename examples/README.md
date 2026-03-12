# WorkflowAsList Examples

Real-world workflow examples.

---

## Structure

```
examples/
├── git/commit.workflow.list    # Git commit helper
├── ci-cd/                      # CI/CD workflows (TBD)
└── research/                   # Research workflows (TBD)
```

Format: `examples/[domain]/[use-case].workflow.list`

---

## Usage

```bash
# Copy example
cp examples/git/commit.workflow.list ./my.workflow.list

# Check and run
workflow check my.workflow.list
workflow approve my
workflow run my
```

---

## Guidelines

Examples must:
- Solve real problems (not toy examples)
- Show DSL features in action
- Include clear comments
- Pass `workflow check`

---

## Examples

### Git

- `git/commit.workflow.list` - Conventional Commits helper

### CI/CD

(TBD)

### Research

(TBD)

---

## Related

- `SYNTAX.md` - DSL syntax
- `README.md` - Project overview

---

Last Updated: 2026-03-12
