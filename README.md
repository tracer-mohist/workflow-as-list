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

Requires Python 3.12+ and uv.

```bash
# Clone repository
git clone https://github.com/tracer-mohist/workflow-as-list.git
cd workflow-as-list

# Install with uv
uv sync

# Install CLI to PATH (optional)
uv pip install -e .
```

---

## Directory Structure

Default state location: `~/.workflow-as-list/`

```
~/.workflow-as-list/
├── config.ini           # Configuration (optional)
├── registry.jsonl       # Registered workflows
├── server.pid           # Server process ID
├── server.log           # Server logs
├── state/
│   ├── executions/      # Execution history
│   └── outputs/         # Step outputs
└── cache/
    └── imports/         # Imported workflow cache
```

To reset all state:
```bash
rm -rf ~/.workflow-as-list/
```

NOTE: Single location for easy cleanup and backup.

---

## Usage

CLI commands:

```bash
# Check and register workflow
workflow check my-workflow.workflow.list

# Approve for execution
workflow approve my-workflow

# Run workflow
workflow run my-workflow

# List all workflows
workflow list

# Show workflow or execution details
workflow show <name-or-id>

# Start HTTP server
workflow serve --host 127.0.0.1 --port 8080
```

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

---

## Vocabulary

Thinking constraint: Limiting output format to reduce divergence
DSL: Domain-Specific Language
Jump: Conditional loop back to tagged item
Tag: Label for referencing items

---

## Documentation

Syntax specification: `SYNTAX.md`, `SYNTAX.ebnf`
Design docs: `docs/design/`
Contributing: `CONTRIBUTING.md`
Commit convention: `.github/COMMIT_CONVENTION.md`

---

## License

MIT

---

Author: Tracer (Chinese: 迹，Ji)
Created: 2026-03-08
Last Updated: 2026-03-12

