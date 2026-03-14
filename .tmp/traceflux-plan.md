<!-- .tmp/traceflux-plan.md -->
# Traceflux Bootstrap Plan

**Status**: Temporary (delete after completion)

**Created**: 2026-03-13

---

## Goal

Use workflow-as-list to manage traceflux development, creating feedback loop.

---

## Phase 1: workflow-as-list Foundation

- [x] Create Issue: "decision-capture workflow" proposal (#39)
- [x] Create `workflow/decision-capture.workflow.list`
- [ ] Test: Process one real decision

---

## Phase 2: traceflux Setup [COMPLETE]

- [x] `traceflux/workflow/README.md` (self-hosting purpose)
- [x] `traceflux/.github/ISSUE_TEMPLATE/decision.yml` (temporary decisions)
- [x] `traceflux/workflow/commit.workflow.list` (remote import test)
  - URL: `https://raw.githubusercontent.com/tracer-mohist/workflow-as-list/refs/heads/main/examples/git/commit.workflow.list`
- [x] `traceflux/workflow/decision-capture.workflow.list` (adapted)
  - URL: `https://raw.githubusercontent.com/tracer-mohist/workflow-as-list/refs/heads/main/examples/decision/route.workflow.list`
- [x] Remote import tested and pushed

NOTE: Both workflows now use `import:` with HTTPS URLs (DSL feature validation)

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
