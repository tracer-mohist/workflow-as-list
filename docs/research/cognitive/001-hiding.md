<!-- docs/research/cognitive/001-hiding.md -->
# Executor Cognitive Hiding

Date: 2026-03-09
Status: Research complete
Author: Tracer

---

## Purpose

Why Executor hides control flow from Agent.

---

## Core Hypothesis

Agents perform better when focused on task, not meta-awareness of control flow.

---

## Cognitive Science Perspectives

### Attention Resource Theory

Attention is limited cognitive resource.

Application to LLMs:
- Context window attention distributed across all tokens
- Awareness of loop counts consumes attention capacity
- Less attention for actual task quality

---

### Task-Focus vs. Meta-Cognition

Human analogy:
- Workers with detailed timelines sometimes game the system
- Knowing deadline = reduced quality in early phases

LLM parallel:
- Agent sees @step-1[3] → knows 3 attempts
- May rush early iterations, save effort for last
- Result: Suboptimal outputs

---

### Observer Effect

Measurement changes the measured system.

Application:
- Agent aware of evaluation criteria optimizes for criteria
- Agent aware of loop structure optimizes for loop exit
- Hiding structure = authentic task engagement

---

## Information Hiding Principle

### What to Hide

- Loop counts: @tag[N] visible to executor, not Agent
- Conditional logic: Exit conditions evaluated by executor
- Import structure: Pre-loaded, transparent to Agent
- Workflow topology: Agent sees linear task list

### What to Expose

- Current step content only
- Relevant context: Previous step outputs (filtered)
- Immediate next action

---

## Executor as Mediator

Flow:
- *.workflow.list (full syntax)
- Executor: Parses all, Evaluates conditions, Filters view
- Agent sees: task content only

WHY: Separates concerns — executor handles flow, Agent handles content.

---

## Expected Benefits

- Consistent quality: Each step treated with equal care
- Reduced gaming: No iteration-count optimization
- Cleaner outputs: Task-focused, not structure-aware
- Better debugging: Executor logs full flow

---

## Open Questions

- Does hiding reduce Agent's ability to self-correct?
- Should some meta-information be optionally exposed?
- How does this interact with Agent's own planning capabilities?

---

REFERENCE: ../encoding/002-ascii.md — Encoding security
REFERENCE: ../../design/overview/001-principles.md — Design principles

---

Last Updated: 2026-03-09
