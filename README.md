<!-- README.md -->
# WorkflowAsList

Workflows are Just Lists.

---

## Purpose

WorkflowAsList is a thinking constraint DSL. It is a minimalist list-based format for structuring LLM interactions and human thinking.

Goal: Filter noise, focus thinking, prevent divergence.

NOTE: This DSL is for thinking constraint, not for execution. LLM reads and follows, no parser needed.

---

## Syntax (5 Rules)

- content                   # List item
 - nested content           # Indent = sub-task (2 spaces)
- (tag) content             # Tag (can modify any line type)
- @tag[N]: condition?       # Jump (max N times)
- import: path              # Import other workflow

Tag Universality: (tag) can modify any line type.

---

## Example

```
- (start) Read project structure
 - Read directory: ls -la
 - Read entry point: cat package.json
 - (analyze) Analyze dependencies

- @analyze[2]: Dependencies clear?

- import: ./common/report.workflow.list

- Generate summary
```

---

## File Extension

- Extension: .workflow.list
- Format: Plain text (UTF-8)

NOTE: Full extension for agent readability. Short forms like .wl reduce clarity.

---

## Design Principles

- Just Lists: No complex syntax
- Constraint over Freedom: Bounded thinking
- Human plus LLM: Readable by both
- 5 Rules Only: If it needs more, it is not WorkflowAsList

---

## Vocabulary Disambiguation

- Thinking constraint: Limiting output format to reduce divergence
- DSL: Domain-Specific Language
- Jump: Conditional loop back to tagged item
- Tag: Label for referencing items

---

## Related

- Specification: Full syntax definition (future)
- Examples: Sample workflows (future)

---

Author: Tracer (Chinese: 迹，Ji)
Created: 2026-03-08
License: MIT
