# WorkflowAsList Examples

Real-world workflow examples.

---

## Structure

```dir.info
examples/
├── git/commit.workflow.list    # Git commit helper
├── ci-cd/                      # CI/CD workflows (TBD)
└── research/                   # Research workflows (TBD)
```

Format: `examples/[domain]/[use-case].workflow.list`

---

## File Header Style

Each workflow file includes a header comment:

```
# =============================================================================
# Workflow: <Name>
# =============================================================================
#
# Purpose: What problem this solves
# Usage: How to run (check, approve, run)
# Preconditions: What must be true before running
# Postconditions: What is guaranteed after running
#
# =============================================================================
```

This follows:
- Traditional script headers (self-documenting)
- Design by Contract (Bertand Meyer) - clear pre/post conditions
- Workflow files are self-contained

---

## Comment Style

Comments explain **why**, not **what**:

```
# Good: explains why
- @validate[1]  # Prevent infinite loops on validation failure

# Bad: explains what (obvious from code)
- @validate[1]  # Jump back to validate tag max 1 time
```

If code needs long comments, refactor the code instead.

This follows Unix philosophy:
- Code should be self-explanatory
- Comments document intent, not mechanics
- Complexity should be refactored, not documented

---

## Guidelines

Examples must:
- Solve real problems (not toy examples)
- Show DSL features in action
- Include clear comments (why, not what)
- Pass `workflow check`

---

## Related

- `SYNTAX.md` - DSL syntax (5 rules)
- `README.md` - Project overview

---

Last Updated: 2026-03-12
