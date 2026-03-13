# Traceflux Bootstrap Plan

**Status**: Temporary (delete after completion)

**Created**: 2026-03-13

---

## Goal

Use workflow-as-list to manage traceflux development, creating feedback loop.

---

## Phase 1: workflow-as-list Foundation

- [ ] Create Issue: "decision-capture workflow" proposal
- [ ] Create `workflow/decision-capture.workflow.list`
- [ ] Test: Process one real decision

---

## Phase 2: traceflux Setup

- [ ] `traceflux/workflow/README.md` (self-hosting purpose)
- [ ] `traceflux/.github/ISSUE_TEMPLATE/decision.yml` (temporary decisions)
- [ ] `traceflux/workflow/commit.workflow.list` (remote import test)
  - URL: `https://raw.githubusercontent.com/tracer-mohist/workflow-as-list/refs/heads/main/examples/git/commit.workflow.list`
- [ ] `traceflux/scripts/check-code-quality.py` (adapt for traceflux)
- [ ] `traceflux/scripts/check-docs-quality.py` (adapt for traceflux)

---

## Phase 3: Feedback Loop

- [ ] Use workflow to manage traceflux development
- [ ] Record issues → Improve workflow-as-list
- [ ] Document patterns

---

## Cleanup

- [ ] Delete `.tmp/` directory
- [ ] Keep only permanent artifacts (workflows, templates)

---

## Principles

- Issue = Temporary decisions (short lifetime)
- Docs = Permanent rules (functors, not instances)
- Workflow = Automation of decision process

---

Last Updated: 2026-03-13
