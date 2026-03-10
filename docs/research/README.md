<!-- docs/research/README.md -->
# Research Index

Purpose: Theoretical foundations for WorkflowAsList.

Scope: LLM interaction, thinking constraints, DSL design.

---

## Reading Order

For implementers:
1. theory/003-limits.md — Token limits and enforcement
2. cognitive/001-hiding.md — Why hide control flow
3. encoding/002-ascii.md — Why ASCII encoding
4. theory/004-derivation.md — Mathematical derivation

For theorists:
1. theory/004-derivation.md — Mathematical derivation
2. theory/003-limits.md — Application and enforcement
3. cognitive/001-hiding.md — Cognitive science basis
4. encoding/002-ascii.md — Information theory basis

---

## Research Categories

### A. Cognitive Foundations

**cognitive/001-hiding.md**

Purpose: Why Executor hides control flow from Agent.

Key insights:
- Agents perform better focused on task, not meta-awareness
- Hiding loop counts prevents gaming behavior
- Reduces cognitive load, improves per-step quality

RELATED: ../design/overview/001-principles.md

---

### B. Encoding Security

**encoding/002-ascii.md**

Purpose: Why *.workflow.list uses printable ASCII only.

Key insights:
- ASCII reduces encoding entropy (6.57 bits vs 20.09 bits)
- No homoglyph attacks, no hidden characters
- Universal compatibility across platforms

RELATED: ../design/security/005-layers.md

---

### C. Task Length Theory

**theory/003-limits.md**

Purpose: Task description token limits and enforcement rules.

Key insights:
- Effective Context Square Root Formula: [√(N × 0.618), √N]
- For 128k models: 282-358 tokens per step
- Three-layer context model (max, limit, effective)

RELATED: ../design/security/005-layers.md

---

**theory/004-derivation.md**

Purpose: Mathematical derivation of k = √N from Six Degrees of Separation.

Key insights:
- Base formula: L = ln(N) / ln(k)
- Constraint L < 2 yields k = √N
- Golden ratio (0.618) for effective context boundary

Authors: sha_dow, Tracer, DeepSeek

---

## Document Template

For new research documents:

- Title: Clear scope (not format)
- Date: YYYY-MM-DD
- Purpose: 1-2 sentence summary
- Content: Main body (lists, not tables)
- Open questions: What needs validation

---

## Related Indexes

- Design documents: see: ../design/README.md
- Project overview: see: ../../README.md
- Syntax specification: see: ../../SYNTAX.md

---

Status: Active research collection
Last Updated: 2026-03-09
