<!-- AGENTS.md -->
# AGENTS.md - WorkflowAsList Project Guide

Purpose: Project architecture and development conventions.

---

## Architecture Overview

```
workflow-as-list/
├── src/workflow_as_list/    # Source code package
│   ├── __init__.py
│   ├── cli.py               # Typer CLI (7 subcommands)
│   ├── server.py            # FastAPI HTTP server
│   ├── executor/            # Core interpreter (parser, state)
│   ├── security/            # 7-layer security checks
│   ├── models.py            # Pydantic data models
│   └── config.py            # Configuration loading (INI)
│
├── docs/                    # Design and research docs
├── scripts/                 # Utility scripts
├── tests/                   # Test suite
├── pyproject.toml           # Project metadata + dependencies
└── AGENTS.md                # This file
```

---

## Development Conventions

### 360-Line Rule

When a file exceeds 360 lines:
- Convert file to directory (package)
- Split by functionality into submodules
- Original file becomes `__init__.py` with exports

Example:
```
cli.py (360+ lines) → cli/
                       ├── __init__.py
                       ├── check.py
                       ├── approve.py
                       └── ...
```

---

### Code Style

Comments:
- Line comments at critical logic points
- Explain intent (why), not mechanics (what)
- Avoid docstrings for every function

Types:
- Type annotations required for all functions
- Pydantic models for data structures

Naming:
- snake_case for functions/variables
- PascalCase for classes
- UPPERCASE for constants

---

### Security

7-layer check implementation:
1. Encoding (ASCII only)
2. Blacklist (substring match)
3. Token length (282-358 bytes)
4. Feature scan
5. Human audit (status)
6. Whitelist (opt-in)
7. TBD

REFERENCE: `docs/design/security/005-layers.md`

---

## State Management

Files (Single Source of Truth):
- `~/.workflow-as-list/registry.jsonl` — Workflow registry
- `~/.workflow-as-list/executions/` — Execution instances
- `~/.workflow-as-list/outputs/` — Step outputs

CLI and Server Share State:
- Both use same files
- Consistency guaranteed

---

## Dependencies

See: `pyproject.toml` (single source of truth)

Core dependencies:
- fastapi — HTTP server framework
- uvicorn — ASGI server
- typer — CLI framework
- pydantic — Data validation

All managed by uv. Use `uv add <package>` for new dependencies.

---

## Testing

Run with: `uv run pytest`

Test files:
- `tests/test_executor_unit.py` — Executor unit tests
- `tests/test_security_unit.py` — Security layer tests
- `tests/test_cli_component.py` — CLI component tests
- `tests/test_server_component.py` — Server component tests

---

## Related

- Design docs: `docs/design/`
- Syntax spec: `SYNTAX.md`, `SYNTAX.ebnf`
- GitHub Issues: https://github.com/tracer-mohist/workflow-as-list/issues

---

Last Updated: 2026-03-12
Maintainer: Tracer (迹)

## Workflow Automation

This project uses workflow-as-list for process automation.

NOTE: For `.workflow.list` files:
- Documentation: `workflow --help`
- Execute: `workflow check/run/exec <workflow-name>`
- Import caching: Automatic (`.imports/`)

Available workflows:
```bash
workflow list
```

Quick start:
```bash
workflow check <name>   # Validate
workflow run <name>     # Execute
workflow exec read <id> # Read step
workflow exec next <id> # Advance
```


## Workflow Automation

This project uses workflow-as-list for process automation.

NOTE: For `.workflow.list` files, use `workflow --help` or execute:
  workflow check/run/exec <workflow-name>

Quick start:
  workflow list              # List available workflows
  workflow check <name>      # Validate workflow
  workflow run <name>        # Start execution
