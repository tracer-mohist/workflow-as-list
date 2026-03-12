# WorkflowAsList Project TODO

**Purpose**: Track development tasks using workflow-as-list DSL.

**Status**: Active

---

## Development Workflow

- (ci-cd) CI/CD Infrastructure
  - Optimize concurrency for parallel test + lint
  - Add commitlint check (PR only)
  - Add documentation quality check (PR only)
  - Create scripts/check-docs-quality.py

- @ci-cd[1]: All CI/CD checks configured?

- (docs) Documentation Refactor
  - Rewrite README.md (<200 lines, no tables, no **)
  - Rewrite AGENTS.md (reference, don't duplicate)
  - Create CONTRIBUTING.md (dev flow, commit conventions)
  - Apply 6-layer prompt engineering framework

- @docs[1]: All docs follow framework?

- (tests) Test Completion
  - Fix datetime.utcnow() deprecation warnings (3 locations)
  - Write integration tests (~5 tests for critical flows)
  - Write E2E tests (5-8 core user workflows)
  - Set coverage threshold (>85%)

- @tests[1]: All tests passing with coverage?

- (release) v0.1.0 Release
  - Configure branch protection (main branch)
  - Require PR + review + CI status checks
  - Tag v0.1.0 and push
  - Verify semantic-release creates GitHub Release
  - Verify CHANGELOG.md auto-generated

- @release[1]: Release published successfully?

---

## Task Priority

- (priority-high) ci-cd
- (priority-high) tests
- (priority-medium) docs
- (priority-low) release

---

## Definition of Done

- All CI/CD checks pass on push
- All tests pass (coverage >85%)
- Documentation follows 6-layer framework
- v0.1.0 release published to GitHub
- First automated release verified

---

**Created**: 2026-03-12
**Updated**: 2026-03-12
**Next Review**: After ci-cd tasks complete
