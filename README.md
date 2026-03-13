# WorkflowAsList

Workflows are Just Lists.

A thinking constraint DSL for structuring LLM interactions and human thinking.

---

## Purpose

Goal: Filter noise, focus thinking, prevent divergence.

NOTE: This DSL is for thinking constraint, not for execution. LLM reads and follows, no parser needed.

---

## Syntax (5 Rules)

```workflow.list
- content                   # List item
 - nested content           # Indent = sub-task (2 spaces)
- (tag) content             # Tag (can modify any line type)
- @tag[N]: condition?       # Jump (max N times)
- import: path              # Import other workflow
```

Tag Universality: (tag) can modify any line type.

---

## Example

```workflow.list
- (start) Read project structure
 - Read directory: ls -la
 - Read entry point: cat package.json
 - (analyze) Analyze dependencies

- @analyze[2]: Dependencies clear?

- import: ./common/report.workflow.list

- Generate summary
```

---

## Installation

### For Users (pipx)

```bash
# Install from GitHub Releases
pipx install git+https://github.com/tracer-mohist/workflow-as-list.git
```

NOTE: pipx installs in isolated environment, no system pollution.

### For Contributors (uv)

```bash
# Clone repository
git clone https://github.com/tracer-mohist/workflow-as-list.git
cd workflow-as-list

# Install with uv (development mode)
uv sync
```

---

## Directory Structure

Default state location: `~/.workflow-as-list/`

- `config.ini` — Configuration (optional)
- `registry.jsonl` — Registered workflows (append-only)
- `server.pid` — Server process ID
- `server.log` — Server logs
- `state/executions/` — Execution instances
- `state/outputs/` — Step outputs (one file per step)
- `cache/imports/` — Imported workflow cache

To reset all state:
```bash
rm -rf ~/.workflow-as-list/
```

NOTE: Single location for easy cleanup and backup.

---

## Execution Model (Progressive Reading)

workflow-as-list is a **reader**, not an executor. It enables progressive reading of workflows.

### Reader Metaphor

Like reading a book:
1. Open to current page (read step)
2. Read and understand content
3. Turn page when ready (advance)
4. Cannot skip unread pages (enforced)

### Agent Workflow

```
1. workflow run <name>           # Create execution instance
2. workflow exec read <id>       # Read current step (mark as read)
3. [Agent executes operations]   # Using own tools (git, API, etc.)
4. workflow exec next <id>       # Advance to next step (must read first)
5. Repeat steps 2-4 until done
```

### CLI Commands

- `workflow check <file>` — Validate and register workflow
- `workflow approve <name>` — Approve for execution
- `workflow reject <name>` — Reject workflow
- `workflow run <name>` — Create execution instance
- `workflow list` — List all workflows
- `workflow show <name>` — Show workflow definition
- `workflow exec read <id>` — Read current step (mark as read)
- `workflow exec next <id>` — Advance to next step (must read first)
- `workflow server start/stop/status/logs` — Server lifecycle

### Server API

- `GET /workflows` — List workflows
- `GET /workflows/{name}` — Workflow details
- `POST /workflows/{name}/approve` — Approve workflow
- `POST /workflows/{name}/run` — Create execution
- `GET /executions/{id}` — Execution status
- `POST /executions/{id}/next` — Advance step (checks read)

REFERENCE: docs/design/runtime/007-execution.md

---

## File Extension

Extension: .workflow.list
Format: Plain text (UTF-8)

NOTE: Full extension for agent readability. Short forms like .wl reduce clarity.

---

## Design Principles

- Just Lists: No complex syntax
- Constraint over Freedom: Bounded thinking
- Human plus LLM: Readable by both
- 5 Rules Only: If it needs more, it is not WorkflowAsList
- Progressive Reading: Must read before advancing

---

## Vocabulary

- Thinking constraint: Limiting output format to reduce divergence
- DSL: Domain-Specific Language
- Jump: Conditional loop back to tagged item
- Tag: Label for referencing items
- Progressive reading: Must read current step before advancing

---

## Documentation

- Syntax specification: `SYNTAX.md`, `SYNTAX.ebnf`
- Design docs: `docs/design/`
- Contributing: `CONTRIBUTING.md`
- Commit convention: `.github/COMMIT_CONVENTION.md`
- Agent integration: See Issue #33

## Repository Structure

```
workflow-as-list/
├── README.md              # This file (getting started)
├── LICENSE                # MIT License
├── CONTRIBUTING.md        # Contribution guidelines
├── CHANGELOG.md           # Version history
├── SYNTAX.md              # DSL syntax specification
├── SYNTAX.ebnf            # Formal grammar
│
├── src/                   # Source code
│   └── workflow_as_list/  # Python package
├── tests/                 # Test suite
├── docs/                  # Documentation
├── examples/              # Example workflows
├── scripts/               # Utility scripts
│
├── .github/               # GitHub configuration
│   ├── ISSUE_TEMPLATE/    # Issue templates
│   └── workflows/         # CI/CD workflows
│
├── pyproject.toml         # Python project configuration
└── uv.lock                # Dependency lock file (uv)
```

---

Author: Tracer (Chinese: 迹，Ji)
Created: 2026-03-08
Last Updated: 2026-03-13
