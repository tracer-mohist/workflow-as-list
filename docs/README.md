<!-- docs/README.md -->
# WorkflowAsList Documentation

Purpose: Navigation hub for all project documentation.

Audience: Developers, researchers, LLM agents.

---

## Directory Structure

- docs/README.md — This file (navigation)
- docs/research/ — Theoretical foundations
- docs/design/ — Finalized specifications
- docs/drafts/ — Work-in-progress (deprecated)

NOTE: drafts/ is deprecated. Use research/ for exploratory work.

---

## Document Categories

### research/

Purpose: Theoretical foundations, academic references, comparative studies.

Contains:
- LLM interaction theory
- Thinking constraint research
- DSL design patterns
- Related work analysis

When to use: Background research that informs design decisions.

---

### design/

Purpose: Finalized specifications, architecture decisions, implementation guides.

Contains:
- System architecture
- API specifications
- Protocol definitions
- Implementation roadmaps

When to use: Committed design decisions.

---

### drafts/ (Deprecated)

Status: Deprecated as of 2026-03-09.

Migration:
- Exploratory ideas → research/
- Finalized concepts → design/
- Meeting notes → memory/ (personal workspace)

WHY: Reduces confusion, clarifies document lifecycle.

---

## Documentation Principles

### Writing Style

Follow 6-layer prompt engineering framework:

1. Encoding: ASCII, simple English
2. Structure: Lists (not tables), no emoji, no emphasis symbols
3. Vocabulary: Use consensus terminology
4. Vocabulary: Define ambiguous terms (Concise, Practical, Elegant)
5. Instruction: Positive, directional words
6. Annotation: REFERENCE, NOTE, TIP with WHY

REFERENCE: Full framework in ~/.openclaw/workspace/docs/prompt-engineering/README.md

---

### Annotation Format

Use LABEL: content format:

- NOTE: Clarifications, exceptions, warnings
- TIP: Practical advice, shortcuts
- REFERENCE: External links, foundational concepts
- DECISION: Design decisions with rationale
- WHY: Intent behind decisions

Example:

NOTE: This decision was made on 2026-03-09.

WHY: Reduces parsing ambiguity.

REFERENCE: Full theory in docs/prompt-engineering/annotation-format.md

---

### Document Lifecycle

Flow:
1. Idea → research/ (exploratory)
2. Validated → design/ (finalized)
3. Referenced → README.md (navigation)

Principle: Documents move forward, never backward.

---

## Related Files

- Project root: ../README.md — Quick start
- Syntax spec: ../SYNTAX.md — Human-readable guide
- Formal grammar: ../SYNTAX.ebnf — EBNF specification
- Scripts: ../scripts/ — Automation tools

---

Last Updated: 2026-03-09
Maintainer: Tracer (迹)
